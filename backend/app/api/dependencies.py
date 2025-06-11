from typing import Optional
from uuid import UUID
from fastapi import Request

from app.core.exceptions import JSONException
from app.core.token import verify_access_token


def get_user(request: Request) -> UUID:
    token: Optional[str] = request.cookies.get("access_token")

    if not token:
        raise JSONException(message="Not authenticated!", status_code=401)

    user_id = verify_access_token(token)

    return user_id
