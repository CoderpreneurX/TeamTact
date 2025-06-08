from fastapi import Response
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=30 * 60,  # 30 minutes
        samesite="lax",
        secure=False,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        samesite="lax",
        secure=False,
    )


def set_reset_password_token_cookie(response: JSONResponse, code: str):
    response.set_cookie(
        key="reset_password_token",
        value=code,
        httponly=True,
        max_age=60 * 60,  # 60 minutes
        samesite="lax",
        secure=False,
    )
