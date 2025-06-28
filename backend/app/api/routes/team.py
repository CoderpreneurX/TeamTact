"""
This Module contains the Routes of the APIs associated with Teams, TeamMates, and Invitations
"""

from fastapi import APIRouter
from app.api.endpoints.team import (
    create_team_endpoint,
    list_teams_endpoint,
    get_team_endpoint,
    delete_team_endpoint,
    # placeholder for future endpoints
)

router = APIRouter(prefix="/teams", tags=["team"])

router.add_api_route(path="/", endpoint=create_team_endpoint, methods=["POST"])
router.add_api_route(path="/", endpoint=list_teams_endpoint, methods=["GET"])
router.add_api_route(path="/{team_id}", endpoint=get_team_endpoint, methods=["GET"])
router.add_api_route(
    path="/{team_id}", endpoint=delete_team_endpoint, methods=["DELETE"]
)
