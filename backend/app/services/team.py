import random
import string
from typing import Sequence
from uuid import UUID

from sqlmodel import Session

from app.core.exceptions import JSONException
from app.crud.team import (
    create_team,
    delete_team,
    read_joined_teams,
    read_team_by_id,
    read_teams_by_owner,
)
from app.models.team import Team
from app.schemas.team import TeamCreateRequest


def _generate_team_code(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def add_team(session: Session, owner_id: UUID, payload: TeamCreateRequest) -> Team:
    existing = read_teams_by_owner(
        session=session, owner_id=owner_id, search=payload.name
    )
    if existing:
        raise JSONException(
            status_code=400, message="A team with this name already exists"
        )
    return create_team(
        session=session,
        owner_id=owner_id,
        name=payload.name,
        code=_generate_team_code(),
    )


def get_team(session: Session, team_id: UUID) -> Team:
    team = read_team_by_id(session=session, team_id=team_id)
    if not team:
        raise JSONException(status_code=404, message="Team not found")
    return team


def get_teams(
    session: Session, owner_id: UUID, team_type: str, search: str | None = None
) -> Sequence[Team]:
    if team_type == "created":
        return read_teams_by_owner(session=session, owner_id=owner_id, search=search)
    return read_joined_teams(session=session, user_id=owner_id, search=search)


def drop_team(session: Session, team_id: UUID, owner_id: UUID) -> None:
    team = read_team_by_id(session=session, team_id=team_id)
    if not team or team.owner_id != owner_id:
        raise JSONException(status_code=403, message="You cannot delete this team")
    delete_team(session=session, team=team)
