from typing import Sequence
from uuid import UUID

from sqlmodel import Session, select

from app.models.team import TeamMate, TeamMateRole
from app.models.user import User


def read_team_members_by_team_id(
    session: Session, team_id: UUID, search: str | None = None, role: str | None = None
) -> Sequence[TeamMate]:
    stmt = select(TeamMate).where(TeamMate.team_id == team_id)

    if role:
        stmt = stmt.where(TeamMate.role == role)

    if search:
        stmt = stmt.join(User).where(
            (User.email.ilike(f"%{search}%")) | (User.name.ilike(f"%{search}%"))
        )

    return session.exec(stmt).all()


def read_member_by_email(session: Session, team_id: UUID, member_email: str):
    query = select(TeamMate).join(User).where(
        User.email == member_email,
        TeamMate.team_id == team_id
    )

    return session.exec(query).first()


def create_member(session: Session, team_id: UUID, user_id: UUID, role: TeamMateRole):
    member = TeamMate(
        team_id=team_id,
        user_id=user_id,
        role=role
    )

    session.add(member)
    session.commit()
    session.refresh(member)
    return member
