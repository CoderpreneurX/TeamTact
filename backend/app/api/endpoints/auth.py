from fastapi import Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.core.security import set_auth_cookies, verify_password
from app.core.token import (
    generate_access_token,
    generate_refresh_token,
    verify_refresh_token,
)
from app.crud.auth import create_user, get_user_by_email_or_username
from app.db.session import get_session
from app.schemas.user import UserCreate


def signup_user(
    user_in: UserCreate, response: Response, session: Session = Depends(get_session)
) -> JSONResponse:
    existing_user = get_user_by_email_or_username(
        session, user_in.email, user_in.username
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email or username already registered"
        )

    user = create_user(session, user_in)
    access_token = generate_access_token(str(user.id))
    refresh_token = generate_refresh_token(str(user.id))

    set_auth_cookies(response, access_token, refresh_token)
    return JSONResponse({"success": True, "data": user.to_json()}, status_code=201)


def login_user(
    user_in: UserCreate, response: Response, session: Session = Depends(get_session)
) -> JSONResponse:
    user = get_user_by_email_or_username(session, user_in.email)

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = generate_access_token(str(user.id))
    refresh_token = generate_refresh_token(str(user.id))

    # Create a JSON response
    response = JSONResponse(
        content={"success": True, "data": user.to_json()}, status_code=200
    )

    # Set cookies on THIS response
    set_auth_cookies(response, access_token, refresh_token)

    return response


def refresh_access_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Refresh token not found in cookies"},
        )

    verification_result = verify_refresh_token(refresh_token)

    if isinstance(verification_result, JSONResponse):
        return verification_result  # error response

    user_id = verification_result.get("sub")
    if not user_id:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Invalid token payload: user ID missing",
            },
        )

    new_access_token = generate_access_token(user_id)

    response = JSONResponse(
        status_code=200,
        content={
            "success": True,
            "access_token": new_access_token,
            "message": "Access token refreshed successfully",
        },
    )

    set_auth_cookies(response, new_access_token, refresh_token)

    return response
