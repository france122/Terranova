from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field


class Quest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    quest_type: str  # daily / challenge / side
    exp_reward: int = 50
    condition_type: str
    condition_value: int
    time_limit_days: Optional[int] = Field(default=None)


class UserQuest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    quest_id: int = Field(foreign_key="quest.id")
    progress: int = Field(default=0)
    status: str = Field(default="active")
    assigned_date: date = Field(default_factory=date.today)
    completed_at: Optional[datetime] = Field(default=None)
