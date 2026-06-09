from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Friendship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    friend_id: int = Field(index=True, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StudyGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StudyGroupMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(index=True, foreign_key="studygroup.id")
    user_id: int = Field(index=True, foreign_key="user.id")
    joined_at: datetime = Field(default_factory=datetime.utcnow)
