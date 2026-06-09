"""Learn router: complete and rate knowledge points."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.database import get_session
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.map_service import complete_node, rate_node

router = APIRouter()


class CompleteRequest(BaseModel):
    node_id: str


class RateRequest(BaseModel):
    node_id: str
    stars: int


@router.post("/complete")
def complete_knowledge_point(
    body: CompleteRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Mark a knowledge point as explored."""
    result = complete_node(user.id, body.node_id, session)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/rate")
def rate_knowledge_point(
    body: RateRequest,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Rate a completed knowledge point (1-3 stars)."""
    result = rate_node(user.id, body.node_id, body.stars, session)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
