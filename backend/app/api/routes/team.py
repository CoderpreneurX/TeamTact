from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlmodel import Session
from uuid import UUID
from typing import List
from pydantic import BaseModel, EmailStr

from app.db.session import get_session
from app.api.dependencies import get_user

from app.api.endpoints.team import (
    autogenerate_team_code,
    create_team_view,
    get_user_teams_view,
    invite_users_view,
    accept_invite_view,
    cancel_invite_view,
    list_team_members_view,
    validate_team_code,
)

router = APIRouter(prefix="/teams", tags=["Teams"])


class TeamCreate(BaseModel):
    name: str
    code: str


class InvitePayload(BaseModel):
    team_id: UUID
    emails: List[EmailStr]

class ValidateTeamCodePayload(BaseModel):
    code: str


@router.post("/")
def create_team_route(
    payload: TeamCreate,
    session: Session = Depends(get_session),
    owner_id: UUID = Depends(get_user),
):
    return create_team_view(
        name=payload.name, code=payload.code, session=session, owner_id=owner_id
    )


@router.post("/invite")
def invite_users_route(payload: InvitePayload, background_tasks: BackgroundTasks = BackgroundTasks(), session: Session = Depends(get_session)):
    return invite_users_view(payload.team_id, payload.emails, session, background_tasks)


@router.get("/accept-invite")
def accept_invite_route(
    team_code: str = Query(..., alias="team_code"),
    session: Session = Depends(get_session),
    current_user: UUID = Depends(get_user),
):
    return accept_invite_view(team_code, session, current_user)


@router.get("/autogenerate-code")
def autogenerate_team_code_route(session: Session = Depends(get_session)):
    return autogenerate_team_code(session)


@router.post("/validate-code")
def validate_code_route(code: ValidateTeamCodePayload, session: Session = Depends(get_session)):
    return validate_team_code(session, code.code)


@router.post("/cancel-invite")
def cancel_invite_route(
    token: str = Query(...), session: Session = Depends(get_session)
):
    return cancel_invite_view(token, session)


@router.get("/")
def user_teams_route(user_id: UUID = Depends(get_user), session: Session = Depends(get_session)):
    return get_user_teams_view(user_id, session)


@router.get("/{team_id}/members")
def list_team_members_route(team_id: UUID, session: Session = Depends(get_session)):
    return list_team_members_view(team_id, session)
