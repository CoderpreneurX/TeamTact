from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session
from app.api.dependencies import get_user
from app.api.endpoints.team import create_team_view, send_invites_view
from app.db.session import get_session
from app.schemas.team import InviteRequest, TeamCreate

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/")
def create_team_route(team_data: TeamCreate, session: Session = Depends(get_session), current_user = Depends(get_user)):
    return create_team_view(team_data, session, current_user)

@router.post("/{team_id}/invite")
def send_invites_route(team_id: UUID, invite_data: InviteRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session), current_user = Depends(get_user)):
    return send_invites_view(team_id, invite_data, background_tasks, session, current_user)
