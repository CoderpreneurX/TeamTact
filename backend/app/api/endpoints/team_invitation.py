from uuid import UUID

from fastapi import BackgroundTasks, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.api.dependencies import get_user
from app.core.helpers import Paginator
from app.db.session import get_session
from app.models.team import TeamMateRole
from app.schemas.team_invitation import InvitationCreateRequest, InvitationResponse
from app.services.team_invitation import (
    get_available_filters,
    get_invitations,
    handle_invitations,
    handle_accept_invitation,
    handle_delete_invitation
)


def list_invitations_endpoint(
    team_id: UUID,
    session: Session = Depends(get_session),
    search: str = Query(None),
    role: TeamMateRole = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    invitations = get_invitations(
        session=session,
        team_id=team_id,
        search=search,
        role=role,
    )

    paginator = Paginator(
        data=invitations, page=page, page_size=per_page, schema=InvitationResponse
    )
    paginated = paginator.paginate()

    return JSONResponse(
        content={
            "success": True,
            "message": "Invitations fetched successfully",
            "data": {"filters": get_available_filters(), "pagination": paginated},
        }
    )


def create_invitations_endpoint(
    data: InvitationCreateRequest,
    team_id: UUID,
    background_tasks: BackgroundTasks,
    user_id: UUID = Depends(get_user),
    session: Session = Depends(get_session),
):
    invitations_data = handle_invitations(
        session=session,
        team_id=team_id,
        invited_by=user_id,
        request_data=data.invitations,
        background_tasks=background_tasks,
    )

    sent_invitations = invitations_data.get("sent_invitations", {})
    unsent_invitations = invitations_data.get("unsent_invitations", {})
    success = False
    message = "Invitations couldn't be processed!"

    if len(unsent_invitations) == 0:
        message = "Invitations sent!"
        success = True

    elif len(sent_invitations) > 0 and len(unsent_invitations) > 0:
        message = "Some invitations couldn't be processed!"

    return JSONResponse(
        content={"success": success, "message": message, "data": invitations_data},
        status_code=200 if success else 400,
    )


def accept_invitation_endpoint(
    invitation_token: str,
    session: Session = Depends(get_session),
    user_id: UUID = Depends(get_user),
):
    member = handle_accept_invitation(
        session=session, invitation_token=invitation_token, user_id=user_id
    )
    return JSONResponse(
        content={
            "success": True,
            "message": "Invitation accepted successfully",
            "data": member,
        }
    )


def delete_invitation_endpoint(
    invitation_id: UUID,
    session: Session = Depends(get_session),
    _: UUID = Depends(get_user),
):
    handle_delete_invitation(
        session=session, invitation_id=invitation_id
    )

    return JSONResponse(
        content={"success": True, "message": "Team deleted successfully!"}
    )
