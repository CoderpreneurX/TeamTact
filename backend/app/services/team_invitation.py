from datetime import datetime
from typing import Any, Dict, List, Tuple
from uuid import UUID

from fastapi import BackgroundTasks
from sqlmodel import Session

from app.core.email import render_template, send_email
from app.core.config import settings
from app.core.exceptions import JSONException
from app.crud.auth import get_user_by_id
from app.crud.team import read_team_by_id
from app.crud.team_invitation import (
    create_invitation,
    drop_invitation,
    mark_invitation_as_accepted,
    read_invitation_by_id,
    read_invitation_by_token,
    read_invitations_by_team_id,
    is_member_invited,
)
from app.crud.team_member import create_member, read_member_by_email
from app.models.team import Team, TeamMateRole
from app.schemas.team_invitation import InvitationData


def get_invitations(session: Session, team_id: UUID, search: str, role: TeamMateRole):
    _get_team(session=session, team_id=team_id)
    invitations = read_invitations_by_team_id(
        session=session, team_id=team_id, search=search, role=role
    )
    return invitations


def get_available_filters():
    return {"roles": [role.value for role in TeamMateRole]}


def _get_team(session: Session, team_id: UUID) -> Team:
    team = read_team_by_id(session=session, team_id=team_id)
    if not team:
        raise JSONException(status_code=404, message="Team not found")
    return team


def _get_invitation(session: Session, invitation_token: str):
    invitation = read_invitation_by_token(
        session=session, invitation_token=invitation_token
    )
    if not invitation:
        raise JSONException(
            message={
                "title": "Invalid Invitation",
                "description": "The link you've followed is invalid",
            },
            status_code=404,
        )
    return invitation


def is_existing_member(session: Session, team_id: UUID, email: str):
    return (
        read_member_by_email(session=session, team_id=team_id, member_email=email)
        is not None
    )


def is_already_invited(session: Session, team_id: UUID, email: str):
    return is_member_invited(session=session, team_id=team_id, member_email=email)


def process_invitation(
    session: Session, team_id: UUID, invited_by: UUID, invitation: InvitationData
) -> Tuple[bool, str, Any]:
    email = invitation.email
    role = invitation.role

    if role == TeamMateRole.OWNER:
        return False, "Owner is created with the team and cannot be invited", None

    if is_existing_member(session, team_id, email):
        return False, "Member already exists", None

    if is_already_invited(session, team_id, email):
        return False, "Member already invited", None

    invitation_instance = create_invitation(session, team_id, invited_by, invitation)
    return True, "", invitation_instance


def handle_invitations(
    session: Session,
    team_id: UUID,
    invited_by: UUID,
    request_data: List[InvitationData],
    background_tasks: BackgroundTasks,
) -> Dict[str, Any]:
    team = _get_team(session=session, team_id=team_id)
    sent_invitations: List[str] = []
    unsent_invitations: List[Dict[str, str]] = []

    for invitation in request_data:
        success, reason, instance = process_invitation(
            session, team_id, invited_by, invitation
        )

        if success:
            sent_invitations.append(invitation.email)

            # Prepare email context
            context = {
                "team_name": team.name,
                "role": invitation.role,
                "invite_link": f"{settings.FRONTEND_DOMAIN}accept-invite?token={instance.token}",
            }

            html_body = render_template("invite.html", **context)

            background_tasks.add_task(
                send_email,
                subject="[TeamTact] You've been invited to join a team!",
                to_email=invitation.email,
                html_body=html_body,
            )
        else:
            unsent_invitations.append({"email": invitation.email, "reason": reason})

    return {
        "sent_invitations": sent_invitations,
        "unsent_invitations": unsent_invitations,
    }


def handle_accept_invitation(session: Session, user_id: UUID, invitation_token: str):
    invitation = _get_invitation(session=session, invitation_token=invitation_token)

    user = get_user_by_id(session=session, user_id=user_id)

    if not invitation.email == user.email:
        raise JSONException(message={
            "title": "Unintented Invitation",
            "description": "The invitation was not intended for you"
        }, status_code=403)
    
    elif invitation.is_accepted:
        raise JSONException(message={
            "title": "Invitation already accepted",
            "description": "The invitation has already been accepted by you"
        })
    
    elif invitation.expiration_date >= datetime.utcnow():
        raise JSONException(message={
            "title": "Invitation Expired",
            "description": "The invitation has been expired"
        })

    elif not _get_team(session=session, team_id=invitation.team_id):
        raise JSONException(message={
            "title": "Team Deleted",
            "description": "The team that you've been invited to, no longer exists"
        })
    
    else:
        mark_invitation_as_accepted(session=session, invitation=invitation)
        member = create_member(session=session, team_id=invitation.team_id, user_id=user_id, role=invitation.role)
        return member


def handle_delete_invitation(session: Session, invitation_id: UUID):
    invitation = read_invitation_by_id(session=session, invitation_id=invitation_id)

    if not invitation:
        raise JSONException(message="Invitation not found", status_code=404)
    
    drop_invitation(session=session, invitation_id=invitation_id)

    return True
