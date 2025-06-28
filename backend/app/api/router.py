from fastapi import APIRouter
from app.api.routes.auth import router as auth_router
from app.api.routes.team import router as team_router
from app.api.routes.team_member import router as team_member_router
from app.api.routes.team_invitation import router as team_invitation_router

# Import individual routers here (e.g. auth_router, team_router, etc.)
# from app.api.endpoints import auth, team, tasks, ...

router = APIRouter()

# You can include your feature routers here, like:
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
# router.include_router(team.router, prefix="/teams", tags=["teams"])

router.include_router(auth_router)
router.include_router(team_router)
router.include_router(team_member_router)
router.include_router(team_invitation_router)
