"""Authentication router: register and login."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    password: str
    nickname: str = ""


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest, session: Session = Depends(get_session)):
    # Check duplicate username
    existing = session.exec(select(User).where(User.username == body.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = User(
        username=body.username,
        hashed_password=hash_password(body.password),
        nickname=body.nickname or body.username,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@router.get("/me")
def get_me(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    from app.models.progress import UserProgress

    explored = session.exec(
        select(UserProgress).where(
            UserProgress.user_id == user.id,
            UserProgress.status.in_(["explored", "mastered"]),
        )
    ).all()
    mastered = [p for p in explored if p.status == "mastered"]
    from app.config import LEVEL_THRESHOLDS

    sorted_levels = sorted(LEVEL_THRESHOLDS.items(), key=lambda x: x[1])
    next_threshold = None
    current_threshold = 0
    for title, threshold in sorted_levels:
        if threshold <= user.exp:
            current_threshold = threshold
        if threshold > user.exp:
            next_threshold = threshold
            break
    # If at max level, use current threshold as cap
    if next_threshold is None:
        next_threshold = current_threshold
    return {
        "id": user.id,
        "username": user.username,
        "nickname": user.nickname,
        "exp": user.exp,
        "level": user.level,
        "exp_to_next": next_threshold,
        "streak_days": user.streak_days,
        "explored_count": len(explored),
        "mastered_count": len(mastered),
    }


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == body.username)).first()
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)
