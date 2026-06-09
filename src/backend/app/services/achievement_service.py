"""Achievement checking and seeding."""
from datetime import datetime
from typing import List, Dict

from sqlmodel import Session, select

from app.models.achievement import Achievement, UserAchievement
from app.models.progress import UserProgress
from app.models.user import User


def check_achievements(user_id: int, session: Session) -> List[Dict]:
    """
    Check all unearned achievements against the user's current stats.
    Returns a list of newly earned achievement dicts.
    """
    # Get all achievements
    all_achievements = session.exec(select(Achievement)).all()

    # Get already earned
    earned_stmt = select(UserAchievement).where(UserAchievement.user_id == user_id)
    earned_ids = {ua.achievement_id for ua in session.exec(earned_stmt).all()}

    # Get user stats
    user = session.get(User, user_id)
    if user is None:
        return []

    # Count explored nodes
    explored_stmt = select(UserProgress).where(
        UserProgress.user_id == user_id,
        UserProgress.status.in_(["explored", "mastered"]),  # type: ignore[union-attr]
    )
    explored_count = len(session.exec(explored_stmt).all())

    # Count mastered nodes
    mastered_stmt = select(UserProgress).where(
        UserProgress.user_id == user_id,
        UserProgress.status == "mastered",
    )
    mastered_count = len(session.exec(mastered_stmt).all())

    newly_earned = []
    for ach in all_achievements:
        if ach.id in earned_ids:
            continue

        earned = False
        if ach.condition_type == "explore_count" and explored_count >= ach.condition_value:
            earned = True
        elif ach.condition_type == "master_count" and mastered_count >= ach.condition_value:
            earned = True
        elif ach.condition_type == "streak_days" and user.streak_days >= ach.condition_value:
            earned = True
        elif ach.condition_type == "exp_total" and user.exp >= ach.condition_value:
            earned = True

        if earned:
            ua = UserAchievement(
                user_id=user_id,
                achievement_id=ach.id,  # type: ignore[arg-type]
                earned_at=datetime.utcnow(),
            )
            session.add(ua)
            newly_earned.append({
                "id": ach.id,
                "key": ach.key,
                "name": ach.name,
                "description": ach.description,
                "icon": ach.icon,
                "category": ach.category,
            })

    if newly_earned:
        session.flush()

    return newly_earned


def get_user_achievements(user_id: int, session: Session) -> List[Dict]:
    """Return all achievements with the user's earned status."""
    all_achievements = session.exec(select(Achievement)).all()

    earned_stmt = select(UserAchievement).where(UserAchievement.user_id == user_id)
    earned_map = {}
    for ua in session.exec(earned_stmt).all():
        earned_map[ua.achievement_id] = ua.earned_at

    result = []
    for ach in all_achievements:
        result.append({
            "id": ach.id,
            "key": ach.key,
            "name": ach.name,
            "description": ach.description,
            "icon": ach.icon,
            "category": ach.category,
            "condition_type": ach.condition_type,
            "condition_value": ach.condition_value,
            "earned": ach.id in earned_map,
            "earned_at": earned_map[ach.id].isoformat() if ach.id in earned_map else None,
        })
    return result
