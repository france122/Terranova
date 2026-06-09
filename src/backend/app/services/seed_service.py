"""Seed service: populate initial achievements and quest templates."""
from typing import List

from sqlmodel import Session, select

from app.models.achievement import Achievement
from app.models.quest import Quest


def seed_initial_data(session: Session) -> None:
    """Create default achievements and quest templates if they don't exist."""
    _seed_achievements(session)
    _seed_quests(session)
    session.commit()


def _seed_achievements(session: Session) -> None:
    """Seed achievement definitions."""
    achievements = [
        # Exploration milestones
        Achievement(
            key="first_step",
            name="第一步",
            description="完成第一个知识点的学习",
            icon="foot",
            category="milestone",
            condition_type="explore_count",
            condition_value=1,
        ),
        Achievement(
            key="explorer_10",
            name="初级探索者",
            description="累计探索10个知识点",
            icon="compass",
            category="milestone",
            condition_type="explore_count",
            condition_value=10,
        ),
        Achievement(
            key="explorer_25",
            name="资深探索者",
            description="累计探索25个知识点",
            icon="map",
            category="milestone",
            condition_type="explore_count",
            condition_value=25,
        ),
        # Mastery achievements
        Achievement(
            key="master_5",
            name="精通之路",
            description="精通5个知识点（3星）",
            icon="star",
            category="mastery",
            condition_type="master_count",
            condition_value=5,
        ),
        Achievement(
            key="master_15",
            name="知识大师",
            description="精通15个知识点（3星）",
            icon="crown",
            category="mastery",
            condition_type="master_count",
            condition_value=15,
        ),
        # Streak achievements
        Achievement(
            key="streak_3",
            name="坚持不懈",
            description="连续学习3天",
            icon="fire",
            category="streak",
            condition_type="streak_days",
            condition_value=3,
        ),
        Achievement(
            key="streak_7",
            name="一周达人",
            description="连续学习7天",
            icon="flame",
            category="streak",
            condition_type="streak_days",
            condition_value=7,
        ),
        Achievement(
            key="streak_30",
            name="月度之星",
            description="连续学习30天",
            icon="trophy",
            category="streak",
            condition_type="streak_days",
            condition_value=30,
        ),
        # EXP milestones
        Achievement(
            key="exp_500",
            name="入门学徒",
            description="累计获得500经验值",
            icon="book",
            category="milestone",
            condition_type="exp_total",
            condition_value=500,
        ),
        Achievement(
            key="exp_5000",
            name="经验丰富",
            description="累计获得5000经验值",
            icon="shield",
            category="milestone",
            condition_type="exp_total",
            condition_value=5000,
        ),
    ]

    for ach in achievements:
        existing = session.exec(
            select(Achievement).where(Achievement.key == ach.key)
        ).first()
        if existing is None:
            session.add(ach)


def _seed_quests(session: Session) -> None:
    """Seed quest templates."""
    quests = [
        # Daily quests
        Quest(
            title="每日一学",
            description="今天完成1个新知识点的学习",
            quest_type="daily",
            exp_reward=50,
            condition_type="complete_node",
            condition_value=1,
        ),
        Quest(
            title="勤学苦练",
            description="今天完成2个新知识点的学习",
            quest_type="daily",
            exp_reward=120,
            condition_type="complete_node",
            condition_value=2,
        ),
        # Challenge quests
        Quest(
            title="数据结构入门挑战",
            description="在7天内完成线性表章节的所有知识点",
            quest_type="challenge",
            exp_reward=200,
            condition_type="complete_node",
            condition_value=3,
            time_limit_days=7,
        ),
        Quest(
            title="速通挑战",
            description="在3天内完成5个知识点",
            quest_type="challenge",
            exp_reward=300,
            condition_type="complete_node",
            condition_value=5,
            time_limit_days=3,
        ),
        Quest(
            title="精通挑战",
            description="将3个知识点提升到3星精通",
            quest_type="challenge",
            exp_reward=250,
            condition_type="master_node",
            condition_value=3,
        ),
    ]

    # Only seed if no quests exist
    existing_count = len(session.exec(select(Quest)).all())
    if existing_count == 0:
        for q in quests:
            session.add(q)
