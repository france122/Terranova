from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Achievement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(unique=True)
    name: str
    description: str
    icon: str = ""
    category: str = "milestone"
    condition_type: str
    condition_value: int


class UserAchievement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    achievement_id: int = Field(foreign_key="achievement.id")
    earned_at: datetime = Field(default_factory=datetime.utcnow)
