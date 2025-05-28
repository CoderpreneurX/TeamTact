from fastapi import Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.api.dependencies import get_user
from app.db.session import get_session
from app.schemas.team import TeamCreate, InviteRequest
from app.crud import team as team_crud
from app.core.email import send_invite_email


def create_team_view(
    team_data: TeamCreate,
    session: Session,
    current_user,
):
    print("Hitting team create API")
    if isinstance(current_user, JSONResponse):
        return current_user

    team = team_crud.create_team(session=session, name=team_data.name, owner_id=current_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"success": True, "message": "Team created", "data": team.dict()},
    )


def send_invites_view(
    team_id: UUID,
    invite_data: InviteRequest,
    background_tasks: BackgroundTasks,
    session: Session,
    current_user,
):
    print("Inviting team members")
    if isinstance(current_user, JSONResponse):
        return current_user

    team = team_crud.get_team_by_id(session, team_id)
    if not team or team.owner_id != current_user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"success": False, "message": "Team not found or access denied", "data": None},
        )

    sent_emails: List[str] = []

    for email in invite_data.emails:
        existing = session.exec(
            select(team_crud.TeamMate).where(
                team_crud.TeamMate.team_id == team_id,
                team_crud.TeamMate.email == email,
                team_crud.TeamMate.cancelled == False,
                team_crud.TeamMate.joined == False,
            )
        ).first()

        if existing:
            continue

        invite = team_crud.invite_teammate(session=session, team_id=team_id, email=email)
        invite_link = f"http://localhost:8000/join?token={invite.invite_token}"

        # Schedule email to be sent in background
        background_tasks.add_task(send_invite_email, email, invite_link, team.name)

        sent_emails.append(email)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "success": True,
            "message": f"Invites sent to {len(sent_emails)} recipient(s).",
            "data": {"invited_emails": sent_emails},
        },
    )
