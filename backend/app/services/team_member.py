from typing import List, Sequence
from uuid import UUID

from sqlmodel import Session

from app.crud.team_member import read_team_members_by_team_id
from app.models.team import TeamMate, TeamMateRole


def get_team_members(
    session: Session, team_id: UUID, search: str | None = None, role: str | None = None
) -> Sequence[TeamMate]:
    return read_team_members_by_team_id(
        session=session, team_id=team_id, search=search, role=role
    )


def get_available_roles() -> List[str]:
    return [role.value for role in TeamMateRole]
