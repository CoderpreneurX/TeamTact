from typing import List
from uuid import UUID

from fastapi import BackgroundTasks

from app.crud.team import (
    accept_invitation,
    cancel_invitation,
    create_team,
    get_invitation_by_email,
    get_team_members,
    get_user_teams,
    invite_teammate,
    is_code_unique,
)
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.schemas.team import InvitationRead, TeamMateRead, TeamRead
from app.services.team import generate_unique_team_code, queue_team_invite_email
from app.core.config import settings

# ---------- TEAM VIEWS ----------


def create_team_view(name: str, code: str, session: Session, owner_id: UUID):
    team = create_team(session, name, code, owner_id)
    return JSONResponse(
        content={
            "success": True,
            "message": "Team created successfully.",
            "data": TeamRead.model_validate(team).model_dump(mode="json"),
        }
    )


def autogenerate_team_code(session: Session):
    code = generate_unique_team_code(session)

    if code:
        return JSONResponse(
            content={
                "success": True,
                "message": "Team Code generated successfully!",
                "data": {"code": code},
            },
            status_code=200,
        )

    return JSONResponse(
        content={"success": False, "message": "Couldn't generate a Unique Team Code!"},
        status_code=400,
    )


def validate_team_code(session: Session, code):
    if is_code_unique(session, code):
        return JSONResponse(
            content={"success": True, "message": "Team Code is Unique!"},
            status_code=200,
        )

    return JSONResponse(
        content={"success": False, "message": "Team Code has already been taken!"},
        status_code=400,
    )


def get_user_teams_view(user_id: UUID, session: Session):
    teams = get_user_teams(session, user_id)
    return JSONResponse(
        content={
            "success": True,
            "message": "User's teams fetched successfully.",
            "data": [
                TeamRead.model_validate(team).model_dump(mode="json") for team in teams
            ],
        }
    )


# ---------- INVITATION VIEWS ----------


def invite_users_view(
    team_id: UUID,
    emails: List[str],
    session: Session,
    background_tasks: BackgroundTasks,
):
    invitations = []

    for email in emails:
        existing = get_invitation_by_email(session, team_id, email)
        if existing:
            invitations.append(existing)
        else:
            invitation = invite_teammate(session, team_id, email)
            invitations.append(invitation)

            # Queue background email sending
            invite_link = f"{settings.FRONTEND_DOMAIN}accept-invite/{invitation.token}"
            queue_team_invite_email(
                background_tasks,
                to_email=email,
                invite_link=invite_link,
                team_name=invitation.team.name if invitation.team else "",
            )

    return JSONResponse(
        content={
            "success": True,
            "message": "Invitations processed.",
            "data": [
                InvitationRead.model_validate(inv).model_dump(mode="json")
                for inv in invitations
            ],
        }
    )


def accept_invite_view(token: str, session: Session, current_user: UUID):
    team_mate = accept_invitation(session, token, current_user)
    if not team_mate:
        return JSONResponse(
            content={
                "success": False,
                "message": "Invite has expired, is invalid, or has been cancelled.",
            }
        )
    return JSONResponse(
        content={
            "success": True,
            "message": f"Invitation to join {team_mate.team.name if team_mate.team else None} accepted successfully!",
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
            "data": [
                TeamMateRead.model_validate(member).model_dump(mode="json")
                for member in members
            ],
        }
    )
