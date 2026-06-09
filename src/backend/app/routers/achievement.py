from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.achievement_service import get_user_achievements

router = APIRouter()


@router.get("/")
def list_achievements(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_user_achievements(user.id, session)
