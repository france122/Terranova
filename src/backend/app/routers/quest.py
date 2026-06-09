from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.quest_service import get_daily_quests, get_challenge_quests, complete_quest

router = APIRouter()


@router.get("/daily")
def daily_quests(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_daily_quests(user.id, session)


@router.get("/challenges")
def challenge_quests(session: Session = Depends(get_session)):
    return get_challenge_quests(session)


@router.post("/{quest_id}/complete")
def finish_quest(
    quest_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    result = complete_quest(user.id, quest_id, session)
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result
