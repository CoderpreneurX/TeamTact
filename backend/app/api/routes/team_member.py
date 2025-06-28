from fastapi import APIRouter

from app.api.endpoints.team_member import list_teammates_endpoint

router = APIRouter(prefix="/team-members", tags=["Team Members"])

router.add_api_route(
    path="/{team_id}/members", endpoint=list_teammates_endpoint, methods=["GET"]
)
