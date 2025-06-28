from typing import Sequence
from uuid import UUID

from sqlmodel import Session, select

from app.models.team import Invitation, TeamMate
from app.models.user import User
from app.schemas.team_invitation import InvitationData


def read_invitations_by_team_id(
    session: Session,
    team_id: UUID,
    search: str | None = None,
    role: str | None = None,
) -> Sequence[Invitation]:
    query = select(Invitation).where(Invitation.team_id == team_id)

    if role:
        query = query.where(Invitation.role == role)

    if search:
        query = query.where(Invitation.email.ilike(f"%{search}%"))

    return session.exec(query).all()


def is_member_invited(session: Session, team_id: UUID, member_email: str):
    query = select(Invitation).where(
        Invitation.email == member_email, Invitation.team_id == team_id
    )
    return session.exec(query).first()


def create_invitation(
    session: Session, team_id: UUID, invited_by: UUID, invitation_data: InvitationData
) -> Invitation:
    invitation = Invitation(
        team_id=team_id,
        email=invitation_data.email,
        role=invitation_data.role,
        invited_by=invited_by,
    )
    session.add(invitation)
    session.commit()
    session.refresh(invitation)
    return invitation


def read_invitation_by_token(session: Session, invitation_token: str):
    query = select(Invitation).where(Invitation.token == invitation_token)
    return session.exec(query).first()


def mark_invitation_as_accepted(session: Session, invitation: Invitation):
    invitation.is_accepted = True
    session.commit()
    session.refresh(invitation)


def read_invitation_by_id(session: Session, invitation_id: UUID):
    invitation = session.exec(
        select(Invitation).where(Invitation.id == invitation_id)
    ).first()

    return invitation


def drop_invitation(session: Session, invitation_id: UUID):
    invitation = session.exec(
        select(Invitation).where(Invitation.id == invitation_id)
    ).first()

    session.delete(invitation)
    session.commit()
