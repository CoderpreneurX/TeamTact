from typing import List
from uuid import UUID

from app.crud.team import (
    accept_invitation,
    cancel_invitation,
    create_team,
    get_invitation_by_email,
    get_team_members,
    get_user_teams,
    invite_teammate,
)
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.schemas.team import InvitationRead, TeamMateRead, TeamRead

# ---------- TEAM VIEWS ----------


def create_team_view(name: str, owner_id: UUID, session: Session):
    team = create_team(session, name, owner_id)
    return JSONResponse(
        content={
            "success": True,
            "message": "Team created successfully.",
            "data": TeamRead.model_validate(team).model_dump(mode="json"),
        }
    )


def get_user_teams_view(user_id: UUID, session: Session):
    teams = get_user_teams(session, user_id)
    return JSONResponse(
        content={
            "success": True,
            "message": "User's teams fetched successfully.",
            "data": [TeamRead.model_validate(team).model_dump(mode="json") for team in teams],
        }
    )


# ---------- INVITATION VIEWS ----------


def invite_users_view(team_id: UUID, emails: List[str], session: Session):
    invitations = []
    for email in emails:
        existing = get_invitation_by_email(session, team_id, email)
        if existing:
            invitations.append(existing)
        else:
            invitations.append(invite_teammate(session, team_id, email))

    return JSONResponse(
        content={
            "success": True,
            "message": "Invitations processed.",
            "data": [InvitationRead.model_validate(inv).model_dump(mode="json") for inv in invitations],
        }
    )


def accept_invite_view(token: str, session: Session, current_user: UUID):
    team_mate = accept_invitation(session, token, current_user)
    if not team_mate:
        return JSONResponse(
            content={
                "success": False,
                "message": "Invite has expired, is invalid, or has been cancelled.",
                "data": {},
            }
        )
    return JSONResponse(
        content={
            "success": True,
            "message": "Invite accepted successfully!",
            "data": {"team_name": team_mate.team.name if team_mate.team else None},
        }
    )


def cancel_invite_view(token: str, session: Session):
    success = cancel_invitation(session, token)
    if not success:
        return JSONResponse(
            content={
                "success": False,
                "message": "Failed to cancel invitation.",
                "data": {},
            }
        )
    return JSONResponse(
        content={
            "success": True,
            "message": "Invitation cancelled successfully.",
            "data": {},
        }
    )


# ---------- TEAMMATE VIEWS ----------


def list_team_members_view(team_id: UUID, session: Session):
    members = get_team_members(session, team_id)
    return JSONResponse(
        content={
            "success": True,
            "message": "Team members fetched successfully.",
            "data": [TeamMateRead.model_validate(member).model_dump(mode="json") for member in members],
        }
    )
