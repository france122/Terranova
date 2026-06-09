from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class UserProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    node_id: str = Field(index=True)
    status: str = Field(default="locked")  # locked / visible / unlocked / explored / mastered
    stars: int = Field(default=0)
    completed_at: Optional[datetime] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
