from fastapi import APIRouter

# Import individual routers here (e.g. auth_router, team_router, etc.)
# from app.api.endpoints import auth, team, tasks, ...

router = APIRouter()

# You can include your feature routers here, like:
# router.include_router(auth.router, prefix="/auth", tags=["auth"])
# router.include_router(team.router, prefix="/teams", tags=["teams"])

@router.get("/ping")
def ping():
    return {"message": "pong"}
