from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.social_service import (
    get_leaderboard, add_friend, get_friends_progress, create_group, join_group,
)

router = APIRouter()


class AddFriendRequest(BaseModel):
    username: str


class CreateGroupRequest(BaseModel):
    name: str


class JoinGroupRequest(BaseModel):
    group_id: int


@router.get("/leaderboard/{board_type}")
def leaderboard(board_type: str, session: Session = Depends(get_session)):
    return get_leaderboard(board_type, session)


@router.post("/friends/add")
def add_friend_route(
    body: AddFriendRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    friend = session.exec(select(User).where(User.username == body.username)).first()
    if friend is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    result = add_friend(user.id, friend.id, session)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/friends/progress")
def friends_progress(
    domain_id: str = Query("cs"),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_friends_progress(user.id, domain_id, session)


@router.post("/groups/create")
def create_group_route(
    body: CreateGroupRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return create_group(body.name, user.id, session)


@router.post("/groups/join")
def join_group_route(
    body: JoinGroupRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    result = join_group(body.group_id, user.id, session)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
