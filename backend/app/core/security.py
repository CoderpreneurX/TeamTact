from passlib.context import CryptContext
from app.core.config import settings
from typing import Tuple
from datetime import datetime, timezone, timedelta
from jose import jwt
from fastapi import Response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_refresh_tokens(user_id: str) -> Tuple[str, str]:
    now = datetime.now(timezone.utc)

    access_payload = {
        "sub": user_id,
        "type": "access",
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME),
        "iat": now,
    }

    refresh_payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_TIME),
        "iat": now,
    }

    access_token = jwt.encode(
        access_payload, settings.JWT_SECRET_KEY, algorithm="HS256"
    )
    refresh_token = jwt.encode(
        refresh_payload, settings.JWT_REFRESH_SECRET_KEY, algorithm="HS256"
    )

    return access_token, refresh_token


def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=15 * 60,  # 15 minutes
        samesite="Lax",
        secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        samesite="Lax",
        secure=True,
    )
