from typing import Sequence
from uuid import UUID

from sqlmodel import Session, select

from app.models.team import Team, TeamMate, TeamMateRole


def create_team(session: Session, owner_id: UUID, name: str, code: str) -> Team:
    team = Team(name=name, code=code, owner_id=owner_id)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def read_team_by_id(session: Session, team_id: UUID) -> Team | None:
    return session.exec(select(Team).where(Team.id == team_id)).first()


def read_teams_by_owner(
    session: Session, owner_id: UUID, search: str | None = None
) -> Sequence[Team]:
    query = select(Team).where(Team.owner_id == owner_id)
    if search:
        query = query.where(Team.name.ilike(f"%{search}%"))
    return session.exec(query).all()


def read_joined_teams(
    session: Session, user_id: UUID, search: str | None = None
) -> Sequence[Team]:
    query = (
        select(Team)
        .join(TeamMate)
        .where(TeamMate.user_id == user_id, TeamMate.role != TeamMateRole.OWNER)
    )

    if search:
        query = query.where(Team.name.ilike(f"%{search}"))

    return session.exec(query).all()


def delete_team(session: Session, team: Team) -> None:
    session.delete(team)
    session.commit()
