"""Map state management: fog-of-war, node completion, unlocking, tunnels."""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

from sqlmodel import Session, select

from app import graph_data
from app.config import EXP_PER_KNOWLEDGE_POINT, EXP_PER_STAR, LEVEL_THRESHOLDS
from app.models.progress import UserProgress
from app.models.user import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _compute_level(exp: int) -> str:
    """Determine level title based on total EXP."""
    level = "学徒"
    for title, threshold in sorted(LEVEL_THRESHOLDS.items(), key=lambda x: x[1]):
        if exp >= threshold:
            level = title
    return level


def _get_progress_map(
    user_id: int, domain_id: str, session: Session
) -> Dict[str, UserProgress]:
    """Return {node_id: UserProgress} for all progress rows the user has in this domain."""
    all_kp_ids = graph_data.get_all_knowledge_points_in_domain(domain_id)
    statement = select(UserProgress).where(
        UserProgress.user_id == user_id,
        UserProgress.node_id.in_(all_kp_ids),  # type: ignore[union-attr]
    )
    rows = session.exec(statement).all()
    return {r.node_id: r for r in rows}


def _all_prereqs_explored(node_id: str, progress_map: Dict[str, UserProgress]) -> bool:
    """Check whether every PREREQUISITE KP predecessor is explored/mastered."""
    prereqs = graph_data.get_prerequisites(node_id)
    kp_prereqs = [
        p
        for p in prereqs
        if graph_data.get_node(p)
        and graph_data.get_node(p)["node_type"] == "knowledge_point"
    ]
    if not kp_prereqs:
        return True
    for p in kp_prereqs:
        prog = progress_map.get(p)
        if prog is None or prog.status not in ("explored", "mastered"):
            return False
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_user_map_state(user_id: int, domain_id: str, session: Session) -> Dict:
    """
    Return the fog-of-war state of every knowledge-point node in the domain.

    States:
        locked   - not visible at all
        visible  - adjacent to explored, outline visible
        unlocked - prerequisites met, can be entered
        explored - completed learning
        mastered - achieved 3 stars
    """
    all_kps = graph_data.get_all_knowledge_points_in_domain(domain_id)
    entry_nodes = graph_data.get_entry_nodes(domain_id)
    progress_map = _get_progress_map(user_id, domain_id, session)

    # Determine the set of explored node IDs
    explored_ids = {
        nid for nid, p in progress_map.items() if p.status in ("explored", "mastered")
    }

    # Determine visible nodes: neighbours of explored nodes
    visible_ids = set()
    for eid in explored_ids:
        for s in graph_data.get_successors(eid):
            if s not in explored_ids:
                visible_ids.add(s)

    node_states = []
    for nid in all_kps:
        prog = progress_map.get(nid)
        if prog and prog.status in ("explored", "mastered"):
            state = prog.status
            stars = prog.stars
        elif nid in entry_nodes and not explored_ids:
            # First-time user: entry nodes are unlocked
            state = "unlocked"
            stars = 0
        elif nid in entry_nodes and nid not in explored_ids:
            # Entry node not yet explored — check if still unlocked
            state = "unlocked"
            stars = 0
        elif _all_prereqs_explored(nid, progress_map):
            state = "unlocked"
            stars = prog.stars if prog else 0
        elif nid in visible_ids:
            state = "visible"
            stars = 0
        else:
            state = "locked"
            stars = 0

        node_info = graph_data.get_node(nid)
        node_states.append(
            {
                "node_id": nid,
                "name": node_info["name"] if node_info else nid,
                "state": state,
                "stars": stars,
            }
        )

    total = len(all_kps)
    explored_count = len(explored_ids)

    return {
        "domain_id": domain_id,
        "total_nodes": total,
        "explored_count": explored_count,
        "explore_rate": round(explored_count / total * 100, 1) if total else 0,
        "nodes": node_states,
    }


def complete_node(user_id: int, node_id: str, session: Session) -> Dict:
    """
    Mark a knowledge-point as explored.

    Returns dict with: exp_gained, new_level, unlocked_nodes, discovered_tunnels, achievements_earned
    """
    node = graph_data.get_node(node_id)
    if node is None or node["node_type"] != "knowledge_point":
        return {"error": "无效的知识点ID"}

    domain_id = graph_data.get_domain_for_node(node_id)
    if domain_id is None:
        return {"error": "无法确定所属领域"}

    progress_map = _get_progress_map(user_id, domain_id, session)

    # Check prerequisites
    if not _all_prereqs_explored(node_id, progress_map):
        return {"error": "前置知识点未完成"}

    # Check if already explored
    existing = progress_map.get(node_id)
    if existing and existing.status in ("explored", "mastered"):
        return {"error": "该知识点已完成"}

    # Create or update progress
    if existing:
        existing.status = "explored"
        existing.completed_at = datetime.utcnow()
        existing.updated_at = datetime.utcnow()
        session.add(existing)
    else:
        progress = UserProgress(
            user_id=user_id,
            node_id=node_id,
            status="explored",
            completed_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(progress)

    # Award EXP
    user = session.get(User, user_id)
    if user is None:
        return {"error": "用户不存在"}

    exp_gained = EXP_PER_KNOWLEDGE_POINT
    user.exp += exp_gained
    old_level = user.level
    user.level = _compute_level(user.exp)
    new_level = user.level if user.level != old_level else None

    # Update streak
    today_str = date.today().isoformat()
    if user.last_study_date != today_str:
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()
        if user.last_study_date == yesterday_str:
            user.streak_days += 1
        else:
            user.streak_days = 1
        user.last_study_date = today_str

    session.add(user)

    # Determine newly unlocked successors
    unlocked_nodes = []
    for s in graph_data.get_successors(node_id):
        s_node = graph_data.get_node(s)
        if s_node and s_node["node_type"] == "knowledge_point":
            # Re-check with the updated progress
            updated_map = dict(progress_map)
            # Simulate current node being explored
            if node_id not in updated_map:
                updated_map[node_id] = UserProgress(
                    user_id=user_id, node_id=node_id, status="explored"
                )
            else:
                updated_map[node_id].status = "explored"
            if _all_prereqs_explored(s, updated_map):
                unlocked_nodes.append({"id": s, "name": s_node["name"]})

    # Discover tunnels (RELATED_TO edges)
    discovered_tunnels = []
    for r in graph_data.get_related_nodes(node_id):
        r_node = graph_data.get_node(r)
        if r_node:
            discovered_tunnels.append(
                {
                    "id": r,
                    "name": r_node["name"],
                    "description": r_node.get("description", ""),
                }
            )

    # Check achievements (import here to avoid circular dependency)
    from app.services.achievement_service import check_achievements

    achievements_earned = check_achievements(user_id, session)

    # Update quest progress
    from app.services.quest_service import update_quest_progress

    update_quest_progress(user_id, "complete_node", session)

    session.commit()

    return {
        "exp_gained": exp_gained,
        "total_exp": user.exp,
        "new_level": new_level,
        "unlocked_nodes": unlocked_nodes,
        "discovered_tunnels": discovered_tunnels,
        "achievements_earned": achievements_earned,
    }


def rate_node(user_id: int, node_id: str, stars: int, session: Session) -> Dict:
    """Update star rating for an explored node (1-3 stars)."""
    if stars < 1 or stars > 3:
        return {"error": "星级必须在1-3之间"}

    statement = select(UserProgress).where(
        UserProgress.user_id == user_id,
        UserProgress.node_id == node_id,
    )
    progress = session.exec(statement).first()
    if progress is None or progress.status not in ("explored", "mastered"):
        return {"error": "请先完成该知识点的学习"}

    old_stars = progress.stars
    if stars <= old_stars:
        return {"error": "星级只能提升，不能降低"}

    progress.stars = stars
    if stars >= 3:
        progress.status = "mastered"
    progress.updated_at = datetime.utcnow()
    session.add(progress)

    # Bonus EXP for stars
    bonus = (stars - old_stars) * EXP_PER_STAR if stars > old_stars else 0
    if bonus > 0:
        user = session.get(User, user_id)
        if user:
            user.exp += bonus
            user.level = _compute_level(user.exp)
            session.add(user)

    session.commit()

    return {
        "node_id": node_id,
        "stars": stars,
        "status": progress.status,
        "exp_bonus": bonus,
    }
