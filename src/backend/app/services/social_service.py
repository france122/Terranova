"""Social features: leaderboard, friends, study groups."""
from datetime import datetime
from typing import List, Dict, Optional

from sqlmodel import Session, select, col

from app.models.user import User
from app.models.social import Friendship, StudyGroup, StudyGroupMember
from app.models.progress import UserProgress
from app import graph_data


def get_leaderboard(board_type: str, session: Session) -> List[Dict]:
    """
    Return top users for a given board type.
    board_type: 'exp' | 'streak' | 'explore_rate'
    """
    users = session.exec(select(User)).all()

    if board_type == "exp":
        ranked = sorted(users, key=lambda u: u.exp, reverse=True)
    elif board_type == "streak":
        ranked = sorted(users, key=lambda u: u.streak_days, reverse=True)
    elif board_type == "explore_rate":
        # Calculate explore rates
        user_rates = []
        for u in users:
            explored_stmt = select(UserProgress).where(
                UserProgress.user_id == u.id,
                UserProgress.status.in_(["explored", "mastered"]),  # type: ignore[union-attr]
            )
            explored_count = len(session.exec(explored_stmt).all())
            # Total KPs across all domains
            total = sum(graph_data.count_nodes_in_domain(d["id"]) for d in graph_data.get_all_domains())
            rate = round(explored_count / total * 100, 1) if total else 0
            user_rates.append((u, rate))
        user_rates.sort(key=lambda x: x[1], reverse=True)
        return [
            {
                "rank": i + 1,
                "user_id": u.id,
                "username": u.username,
                "nickname": u.nickname,
                "level": u.level,
                "value": rate,
            }
            for i, (u, rate) in enumerate(user_rates[:50])
        ]
    else:
        return []

    return [
        {
            "rank": i + 1,
            "user_id": u.id,
            "username": u.username,
            "nickname": u.nickname,
            "level": u.level,
            "value": u.exp if board_type == "exp" else u.streak_days,
        }
        for i, u in enumerate(ranked[:50])
    ]


def add_friend(user_id: int, friend_id: int, session: Session) -> Dict:
    """Add a bidirectional friendship."""
    if user_id == friend_id:
        return {"error": "不能添加自己为好友"}

    friend = session.get(User, friend_id)
    if friend is None:
        return {"error": "用户不存在"}

    # Check if already friends
    existing = session.exec(
        select(Friendship).where(
            Friendship.user_id == user_id,
            Friendship.friend_id == friend_id,
        )
    ).first()
    if existing:
        return {"error": "已经是好友了"}

    # Create bidirectional friendship
    f1 = Friendship(user_id=user_id, friend_id=friend_id)
    f2 = Friendship(user_id=friend_id, friend_id=user_id)
    session.add(f1)
    session.add(f2)
    session.commit()

    return {"message": "好友添加成功", "friend_id": friend_id, "friend_name": friend.username}


def get_friends_progress(user_id: int, domain_id: str, session: Session) -> List[Dict]:
    """Get exploration progress of all friends in a specific domain."""
    # Get friend IDs
    friendships = session.exec(
        select(Friendship).where(Friendship.user_id == user_id)
    ).all()
    friend_ids = [f.friend_id for f in friendships]

    total_kps = graph_data.count_nodes_in_domain(domain_id)
    all_kps = set(graph_data.get_all_knowledge_points_in_domain(domain_id))

    result = []
    for fid in friend_ids:
        friend = session.get(User, fid)
        if friend is None:
            continue

        explored_stmt = select(UserProgress).where(
            UserProgress.user_id == fid,
            UserProgress.status.in_(["explored", "mastered"]),  # type: ignore[union-attr]
            UserProgress.node_id.in_(all_kps),  # type: ignore[union-attr]
        )
        explored_count = len(session.exec(explored_stmt).all())

        result.append({
            "user_id": fid,
            "username": friend.username,
            "nickname": friend.nickname,
            "level": friend.level,
            "explored_count": explored_count,
            "total_nodes": total_kps,
            "explore_rate": round(explored_count / total_kps * 100, 1) if total_kps else 0,
        })

    return result


def create_group(name: str, owner_id: int, session: Session) -> Dict:
    """Create a new study group."""
    group = StudyGroup(name=name, owner_id=owner_id)
    session.add(group)
    session.flush()

    # Owner auto-joins the group
    member = StudyGroupMember(group_id=group.id, user_id=owner_id)  # type: ignore[arg-type]
    session.add(member)
    session.commit()
    session.refresh(group)

    return {
        "id": group.id,
        "name": group.name,
        "owner_id": group.owner_id,
        "created_at": group.created_at.isoformat(),
    }


def join_group(group_id: int, user_id: int, session: Session) -> Dict:
    """Join an existing study group."""
    group = session.get(StudyGroup, group_id)
    if group is None:
        return {"error": "学习小组不存在"}

    # Check if already a member
    existing = session.exec(
        select(StudyGroupMember).where(
            StudyGroupMember.group_id == group_id,
            StudyGroupMember.user_id == user_id,
        )
    ).first()
    if existing:
        return {"error": "已经是小组成员了"}

    member = StudyGroupMember(group_id=group_id, user_id=user_id)
    session.add(member)
    session.commit()

    return {"message": "加入小组成功", "group_id": group_id, "group_name": group.name}


def get_group_map(group_id: int, domain_id: str, session: Session) -> Dict:
    """Get combined exploration map of all group members."""
    group = session.get(StudyGroup, group_id)
    if group is None:
        return {"error": "学习小组不存在"}

    members = session.exec(
        select(StudyGroupMember).where(StudyGroupMember.group_id == group_id)
    ).all()

    all_kps = graph_data.get_all_knowledge_points_in_domain(domain_id)
    total = len(all_kps)

    # Aggregate visibility: any member's explored node contributes visibility
    combined_explored = set()
    member_details = []
    for m in members:
        user = session.get(User, m.user_id)
        if user is None:
            continue

        explored_stmt = select(UserProgress).where(
            UserProgress.user_id == m.user_id,
            UserProgress.status.in_(["explored", "mastered"]),  # type: ignore[union-attr]
            UserProgress.node_id.in_(set(all_kps)),  # type: ignore[union-attr]
        )
        user_explored = {p.node_id for p in session.exec(explored_stmt).all()}
        combined_explored.update(user_explored)

        member_details.append({
            "user_id": m.user_id,
            "username": user.username,
            "explored_count": len(user_explored),
        })

    return {
        "group_id": group_id,
        "group_name": group.name,
        "domain_id": domain_id,
        "total_nodes": total,
        "combined_explored": len(combined_explored),
        "combined_rate": round(len(combined_explored) / total * 100, 1) if total else 0,
        "members": member_details,
    }
