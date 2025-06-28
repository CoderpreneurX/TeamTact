from fastapi import APIRouter

from app.api.endpoints.team_invitation import (
    list_invitations_endpoint,
    create_invitations_endpoint,
    delete_invitation_endpoint,
)

router = APIRouter(prefix="/team-invitations", tags=["Team Invitations"])

router.add_api_route(
    path="/{team_id}", endpoint=list_invitations_endpoint, methods=["GET"]
)
router.add_api_route(
    path="/{team_id}", endpoint=create_invitations_endpoint, methods=["POST"]
)
router.add_api_route(
    path="/{invitation_id}", endpoint=delete_invitation_endpoint, methods=["DELETE"]
)
