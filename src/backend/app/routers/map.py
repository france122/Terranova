"""Map router: user-specific fog-of-war state."""
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database import get_session
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.map_service import get_user_map_state

router = APIRouter()


@router.get("/state")
def get_map_state(
    domain_id: str = Query(..., description="域ID"),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Return the fog-of-war map state for the current user."""
    return get_user_map_state(user.id, domain_id, session)
