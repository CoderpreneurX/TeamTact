from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.core.helpers import Paginator
from app.db.session import get_session
from app.models.team import TeamMateRole
from app.schemas.team_member import TeamMateResponse
from app.services.team_member import get_available_roles, get_team_members


def list_teammates_endpoint(
    team_id: UUID,
    session: Session = Depends(get_session),
    search: str = Query(None),
    role: TeamMateRole = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    teammates = get_team_members(
        session=session, team_id=team_id, search=search, role=role
    )
    paginator = Paginator(
        data=teammates, page=page, page_size=per_page, schema=TeamMateResponse
    )
    paginated = paginator.paginate()

    # Inject available filters
    filters = {"roles": get_available_roles()}

    return JSONResponse(
        content={
            "success": True,
            "message": "Teammates fetched successfully",
            "data": {"filters": filters, "pagination": paginated},
        }
    )
