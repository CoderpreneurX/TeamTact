from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

from app.models.team import Invitation, Team, TeamMate
from sqlmodel import Session, select

# ----------------------------
# 🏢 TEAM CRUD OPERATIONS
# ----------------------------

def create_team(session: Session, name: str, code: str, owner_id: UUID) -> Team:
    """Create a new team and add the owner as a member."""
    team = Team(name=name, code=code, owner_id=owner_id)
    session.add(team)
    session.commit()
    session.refresh(team)

    # Add owner as a teammate
    teammate = TeamMate(team_id=team.id, user_id=owner_id)
    session.add(teammate)
    session.commit()

    return team


def is_code_unique(session: Session, code: str) -> bool:
    """Check if the provided code is unique, i.e., it is not associated with any existing team"""
    team = session.exec(select(Team).where(Team.code == code)).first()

    if team:
        return False
    
    return True


def get_team_by_id(session: Session, team_id: UUID) -> Optional[Team]:
    return session.exec(select(Team).where(Team.id == team_id)).one_or_none()


# ----------------------------
# 👥 TEAMMATE OPERATIONS
# ----------------------------

def get_team_members(session: Session, team_id: UUID) -> List[TeamMate]:
    """Get all members of a team."""
    return session.exec(select(TeamMate).where(TeamMate.team_id == team_id)).all()


def get_user_teams(session: Session, user_id: UUID) -> List[Team]:
    """Get all teams a user is a member of."""
    return session.exec(
        select(Team).join(Team.members).where(TeamMate.user_id == user_id)
    ).all()


# ----------------------------
# 📩 INVITATION OPERATIONS
# ----------------------------

def invite_teammate(
    session: Session, team_id: UUID, email: str, user_id: Optional[UUID] = None
) -> Invitation:
    """Create and return a new invitation."""
    token = uuid4().hex
    invitation = Invitation(
        team_id=team_id,
        email=email,
        user_id=user_id,
        token=token,
        invited_at=datetime.utcnow(),
        expiration_date=datetime.utcnow() + timedelta(days=3)
    )
    session.add(invitation)
    session.commit()
    session.refresh(invitation)
    return invitation


def accept_invitation(session: Session, token: str, user_id: UUID) -> Optional[TeamMate]:
    """Accept an invitation and add the user as a teammate."""
    invitation = validate_invitation(session, token)
    if not invitation or not invitation.user_id == user_id:
        return None

    teammate = TeamMate(team_id=invitation.team_id, user_id=user_id)
    invitation.is_accepted = True
    invitation.accepted_at = datetime.utcnow()

    session.add(teammate)
    session.commit()
    session.refresh(teammate)
    return teammate


def cancel_invitation(session: Session, token: str) -> bool:
    """Cancel a pending invitation by token."""
    invitation = session.exec(select(Invitation).where(Invitation.token == token)).one_or_none()
    if not invitation or invitation.is_cancelled or invitation.is_accepted:
        return False

    invitation.is_cancelled = True
    session.commit()
    return True


def validate_invitation(session: Session, token: str) -> Optional[Invitation]:
    """Check if the invitation is valid and active."""
    invitation = session.exec(select(Invitation).where(Invitation.token == token)).one_or_none()
    if not invitation:
        return None
    if invitation.is_cancelled or invitation.is_accepted:
        return None
    if invitation.expiration_date < datetime.utcnow():
        return None
    return invitation


def get_invitation_by_email(session: Session, team_id: UUID, email: str) -> Optional[Invitation]:
    """Get a pending invitation by email and team."""
    return session.exec(
        select(Invitation).where(
            Invitation.team_id == team_id,
            Invitation.email == email,
            Invitation.is_cancelled == False,
            Invitation.is_accepted == False
        )
    ).one_or_none()


def cleanup_expired_invitations(session: Session) -> int:
    """Cancel expired invitations that have not been accepted or cancelled."""
    invitations = session.exec(
        select(Invitation).where(
            Invitation.expiration_date < datetime.utcnow(),
            Invitation.is_accepted == False,
            Invitation.is_cancelled == False
        )
    ).all()
    
    for invite in invitations:
        invite.is_cancelled = True

    session.commit()
    return len(invitations)
