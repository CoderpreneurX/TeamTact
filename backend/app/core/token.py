from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.core.exceptions import JSONException

# Secret keys
ACCESS_TOKEN_SECRET = settings.JWT_SECRET_KEY
REFRESH_TOKEN_SECRET = settings.JWT_REFRESH_SECRET_KEY

# Expiration times
ACCESS_TOKEN_EXP_MINUTES = settings.ACCESS_TOKEN_EXPIRATION_TIME
REFRESH_TOKEN_EXP_DAYS = settings.REFRESH_TOKEN_EXPIRATION_TIME


def generate_access_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXP_MINUTES),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm="HS256")


def generate_refresh_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXP_DAYS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm="HS256")


def verify_access_token(token: str) -> UUID:
    try:
        payload = jwt.decode(
            token, ACCESS_TOKEN_SECRET, algorithms=settings.JWT_ALGORITHM
        )
        if payload.get("type") != "access":
            raise JSONException(
                message="Invalid token type: expected access token",
                status_code=401,
            )
        return UUID(payload.get("sub"))
    except ExpiredSignatureError as exc:
        raise JSONException(
            message="Access token has expired",
            status_code=401,
        ) from exc
    except JWTError as exc:
        raise JSONException(
            message="Invalid access token",
            status_code=401,
        ) from exc


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token, REFRESH_TOKEN_SECRET, algorithms=settings.JWT_ALGORITHM
        )
        if payload.get("type") != "refresh":
            raise JSONException(
                message="Invalid token type: expected refresh token",
                status_code=400,
            )
        return payload
    except ExpiredSignatureError as exc:
        raise JSONException(
            message="Refresh token has expired",
            status_code=400,
        ) from exc
    except JWTError as exc:
        raise JSONException(
            message="Invalid refresh token",
            status_code=400,
        ) from exc
