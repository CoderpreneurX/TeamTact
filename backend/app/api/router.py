from fastapi import APIRouter
from app.api.routes.auth import router as auth_router

# Import individual routers here (e.g. auth_router, team_router, etc.)
# from app.api.endpoints import auth, team, tasks, ...

router = APIRouter()

# You can include your feature routers here, like:
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
# router.include_router(team.router, prefix="/teams", tags=["teams"])

router.include_router(auth_router)