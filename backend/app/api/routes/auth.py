from fastapi import APIRouter, Response, Depends
from app.api.endpoints.auth import signup_user, login_user
from app.schemas.user import UserCreate, UserRead, UserLogin
from sqlmodel import Session
from app.db.session import get_session

router = APIRouter()


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