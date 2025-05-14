from fastapi import HTTPException, Response, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead
from app.crud.auth import get_user_by_email_or_username, create_user
from app.core.security import create_access_refresh_tokens, set_auth_cookies, verify_password
from app.db.session import get_session
from app.models.user import User


def signup_user(
    user_in: UserCreate, response: Response, session: Session = Depends(get_session)
) -> UserRead:
    existing_user = get_user_by_email_or_username(
        session, user_in.email, user_in.username
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email or username already registered"
        )

    user = create_user(session, user_in)
    access_token, refresh_token = create_access_refresh_tokens(str(user.id))

    set_auth_cookies(response, access_token, refresh_token)
    return JSONResponse({"success": True, "data": user.to_json()}, status_code=201)

def login_user(
    user_in: UserCreate, response: Response, session: Session = Depends(get_session)
) -> UserRead:
    user = get_user_by_email_or_username(session, user_in.email)

    if not user:
        print("User not found!")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify if the password is correct
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate access and refresh tokens
    access_token, refresh_token = create_access_refresh_tokens(str(user.id))

    # Set tokens as HTTP-only cookies
    set_auth_cookies(response, access_token, refresh_token)

    return JSONResponse({
        "success": True,
        "data": user.to_json()
    }, status_code=200)