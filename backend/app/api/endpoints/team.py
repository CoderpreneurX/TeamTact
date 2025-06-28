from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.api.dependencies import get_user
from app.core.helpers import Paginator
from app.db.session import get_session
from app.schemas.team import TeamCreateRequest, TeamResponse
from app.services.team import add_team, get_team, get_teams, drop_team


def create_team_endpoint(
    payload: TeamCreateRequest,
    user_id: UUID = Depends(get_user),
    session: Session = Depends(get_session),
):
    team = add_team(session=session, owner_id=user_id, payload=payload)
    return JSONResponse(
        content={
            "success": True,
            "message": "Team created successfully",
            "data": TeamResponse.model_validate(team).model_dump(mode="json"),
        }
    )


def list_teams_endpoint(
    user_id: UUID = Depends(get_user),
    session: Session = Depends(get_session),
    team_type: str = Query("created"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
):
    teams = get_teams(
        session=session, owner_id=user_id, team_type=team_type, search=search
    )
    paginator = Paginator(
        data=teams, page=page, page_size=page_size, schema=TeamResponse
    )
    paginated = paginator.paginate()
    return JSONResponse(
        content={
            "success": True,
            "message": "Teams retrieved successfully",
            "data": paginated,
        }
    )


def get_team_endpoint(team_id: UUID, session: Session = Depends(get_session)):
    team = get_team(session=session, team_id=team_id)
    return JSONResponse(
        content={
            "success": True,
            "message": "Team fetched successfully",
            "data": TeamResponse.model_validate(team).model_dump(mode="json"),
        }
    )


def delete_team_endpoint(
    team_id: UUID,
    user_id: UUID = Depends(get_user),
    session: Session = Depends(get_session),
):
    drop_team(session=session, team_id=team_id, owner_id=user_id)
    return JSONResponse(
        content={"success": True, "message": "Team deleted successfully", "data": {}}
    )
