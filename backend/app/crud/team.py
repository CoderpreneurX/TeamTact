from sqlmodel import Session, select
from app.models.team import Team, TeamMate  # assuming your models are in models.py
from uuid import UUID
from typing import Optional, List
from datetime import datetime
import uuid


# --------------------
# Team CRUD Operations
# --------------------

def create_team(session: Session, name: str, owner_id: UUID) -> Team:
    team = Team(name=name, owner_id=owner_id)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def get_team_by_id(session: Session, team_id: UUID) -> Optional[Team]:
    return session.get(Team, team_id)


def get_teams_by_owner(session: Session, owner_id: UUID) -> List[Team]:
    statement = select(Team).where(Team.owner_id == owner_id)
    return session.exec(statement).all()


def delete_team(session: Session, team_id: UUID) -> bool:
    team = session.get(Team, team_id)
    if team:
        session.delete(team)
        session.commit()
        return True
    return False


# ------------------------
# TeamMate CRUD Operations
# ------------------------

def invite_teammate(session: Session, team_id: UUID, email: str) -> TeamMate:
    token = uuid.uuid4().hex
    teammate = TeamMate(team_id=team_id, email=email, invite_token=token)
    session.add(teammate)
    session.commit()
    session.refresh(teammate)
    return teammate


def get_teammate_by_token(session: Session, token: str) -> Optional[TeamMate]:
    statement = select(TeamMate).where(TeamMate.invite_token == token)
    return session.exec(statement).first()


def get_teammates_by_team(session: Session, team_id: UUID) -> List[TeamMate]:
    statement = select(TeamMate).where(TeamMate.team_id == team_id)
    return session.exec(statement).all()


def accept_invite(session: Session, token: str, user_id: UUID) -> Optional[TeamMate]:
    teammate = get_teammate_by_token(session, token)
    if teammate and not teammate.joined and not teammate.cancelled:
        teammate.user_id = user_id
        teammate.joined = True
        teammate.joined_at = datetime.utcnow()
        session.add(teammate)
        session.commit()
        session.refresh(teammate)
        return teammate
    return None


def cancel_invite(session: Session, teammate_id: UUID) -> bool:
    teammate = session.get(TeamMate, teammate_id)
    if teammate and not teammate.joined:
        teammate.cancelled = True
        session.add(teammate)
        session.commit()
        return True
    return False
