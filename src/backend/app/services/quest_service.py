"""Quest management: daily quests, challenge quests, progress tracking."""

from datetime import datetime, date
from typing import List, Dict, Optional

from sqlmodel import Session, select

from app.config import EXP_DAILY_QUEST_BONUS, EXP_CHALLENGE_QUEST_BONUS
from app.models.quest import Quest, UserQuest
from app.models.user import User


def get_daily_quests(user_id: int, session: Session) -> List[Dict]:
    """
    Return today's daily quests for the user.
    If not yet assigned today, assign them from the quest templates.
    """
    today = date.today()

    # Check existing assignments for today
    statement = select(UserQuest).where(
        UserQuest.user_id == user_id,
        UserQuest.assigned_date == today,
    )
    existing = session.exec(statement).all()

    # Filter to daily quests
    daily_assigned = []
    for uq in existing:
        quest = session.get(Quest, uq.quest_id)
        if quest and quest.quest_type == "daily":
            daily_assigned.append(uq)

    if daily_assigned:
        return _format_user_quests(daily_assigned, session)

    # Assign daily quests
    daily_templates = session.exec(
        select(Quest).where(Quest.quest_type == "daily")
    ).all()

    new_assignments = []
    for quest in daily_templates:
        uq = UserQuest(
            user_id=user_id,
            quest_id=quest.id,  # type: ignore[arg-type]
            progress=0,
            status="active",
            assigned_date=today,
        )
        session.add(uq)
        new_assignments.append(uq)

    session.commit()
    # Refresh to get IDs
    for uq in new_assignments:
        session.refresh(uq)

    return _format_user_quests(new_assignments, session)


def get_challenge_quests(session: Session) -> List[Dict]:
    """Return all available challenge quests."""
    quests = session.exec(select(Quest).where(Quest.quest_type == "challenge")).all()
    result = []
    for q in quests:
        result.append(
            {
                "id": q.id,
                "title": q.title,
                "description": q.description,
                "quest_type": q.quest_type,
                "exp_reward": q.exp_reward,
                "condition_type": q.condition_type,
                "condition_value": q.condition_value,
                "time_limit_days": q.time_limit_days,
            }
        )
    return result


def update_quest_progress(user_id: int, condition_type: str, session: Session) -> None:
    """
    Called when the user performs an action (e.g., completing a node).
    Increments progress on all active quests that match the condition_type.
    """
    today = date.today()

    # Get all active user quests
    statement = select(UserQuest).where(
        UserQuest.user_id == user_id,
        UserQuest.status == "active",
    )
    active_quests = session.exec(statement).all()

    for uq in active_quests:
        quest = session.get(Quest, uq.quest_id)
        if quest is None:
            continue
        if quest.condition_type != condition_type:
            continue

        uq.progress += 1

        # Auto-complete if target reached
        if uq.progress >= quest.condition_value:
            uq.status = "completed"
            uq.completed_at = datetime.utcnow()

            # Award EXP and recalculate level
            user = session.get(User, user_id)
            if user:
                user.exp += quest.exp_reward
                from app.services.map_service import _compute_level

                user.level = _compute_level(user.exp)
                session.add(user)

        session.add(uq)

    session.flush()


def complete_quest(user_id: int, quest_id: int, session: Session) -> Dict:
    """Manually complete a quest (for quests that need explicit completion)."""
    statement = select(UserQuest).where(
        UserQuest.user_id == user_id,
        UserQuest.quest_id == quest_id,
        UserQuest.status == "active",
    )
    uq = session.exec(statement).first()
    if uq is None:
        return {"error": "未找到该活跃任务"}

    quest = session.get(Quest, quest_id)
    if quest is None:
        return {"error": "任务不存在"}

    if uq.progress < quest.condition_value:
        return {
            "error": "任务进度未达标",
            "current": uq.progress,
            "required": quest.condition_value,
        }

    uq.status = "completed"
    uq.completed_at = datetime.utcnow()
    session.add(uq)

    # Award EXP and recalculate level
    user = session.get(User, user_id)
    if user:
        user.exp += quest.exp_reward
        from app.services.map_service import _compute_level

        user.level = _compute_level(user.exp)
        session.add(user)

    session.commit()

    return {
        "quest_id": quest_id,
        "status": "completed",
        "exp_reward": quest.exp_reward,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _format_user_quests(user_quests: List[UserQuest], session: Session) -> List[Dict]:
    result = []
    for uq in user_quests:
        quest = session.get(Quest, uq.quest_id)
        if quest is None:
            continue
        result.append(
            {
                "user_quest_id": uq.id,
                "quest_id": quest.id,
                "title": quest.title,
                "description": quest.description,
                "quest_type": quest.quest_type,
                "exp_reward": quest.exp_reward,
                "condition_type": quest.condition_type,
                "condition_value": quest.condition_value,
                "progress": uq.progress,
                "status": uq.status,
                "assigned_date": uq.assigned_date.isoformat(),
            }
        )
    return result
