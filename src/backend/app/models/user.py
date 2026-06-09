from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    nickname: str = ""
    exp: int = Field(default=0)
    level: str = Field(default="学徒")
    streak_days: int = Field(default=0)
    last_study_date: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
