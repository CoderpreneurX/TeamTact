from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from uuid import UUID
from typing import List
from pydantic import BaseModel, EmailStr

from app.db.session import get_session
from app.api.dependencies import get_user

from app.api.endpoints.team import (
    create_team_view,
    get_user_teams_view,
    invite_users_view,
    accept_invite_view,
    cancel_invite_view,
    list_team_members_view
)

router = APIRouter(prefix="/teams", tags=["Teams"])


class TeamCreate(BaseModel):
    name: str
    owner_id: UUID


class InvitePayload(BaseModel):
    team_id: UUID
    emails: List[EmailStr]


@router.post("/")
def create_team_route(
    payload: TeamCreate,
    session: Session = Depends(get_session),
):
    return create_team_view(payload.name, payload.owner_id, session)


@router.post("/invite")
def invite_users_route(
    payload: InvitePayload,
    session: Session = Depends(get_session)
):
    return invite_users_view(payload.team_id, payload.emails, session)


@router.get("/accept-invite")
def accept_invite_route(
    team_code: str = Query(..., alias="team_code"),
    session: Session = Depends(get_session),
    current_user: UUID = Depends(get_user)
):
    return accept_invite_view(team_code, session, current_user)


@router.post("/cancel-invite")
def cancel_invite_route(
    token: str = Query(...),
    session: Session = Depends(get_session)
):
    return cancel_invite_view(token, session)


@router.get("/user/{user_id}")
def user_teams_route(
    user_id: UUID,
    session: Session = Depends(get_session)
):
    return get_user_teams_view(user_id, session)


@router.get("/{team_id}/members")
def list_team_members_route(
    team_id: UUID,
    session: Session = Depends(get_session)
):
    return list_team_members_view(team_id, session)
