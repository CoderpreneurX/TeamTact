from fastapi import APIRouter, Request, Response, Depends
from app.api.dependencies import get_user
from app.api.endpoints.auth import get_profile, refresh_access_token, signup_user, login_user
from app.schemas.user import UserCreate, UserRead, UserLogin
from sqlmodel import Session
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


@router.post("/signup", response_model=UserRead)
def signup_route(
    user_in: UserCreate, response: Response, session: Session = Depends(get_session)
):
    return signup_user(user_in, response, session)

@router.post("/login", response_model=UserRead)
def login_route(
    user_in: UserLogin, response: Response, session: Session = Depends(get_session)
):
    return login_user(user_in, response, session)

@router.get("/refresh-access-token")
def refresh_access_token_route(request: Request):
    return refresh_access_token(request)

@router.get("/me")
def get_profile_route(session: Session = Depends(get_session), user_id: str = Depends(get_user)):
    return get_profile(session=session, user_id=user_id)