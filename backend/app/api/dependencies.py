from typing import Optional
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.token import verify_access_token


def get_user(request: Request) -> str | JSONResponse:
    token: Optional[str] = request.cookies.get("access_token")

    if not token:
        return JSONResponse(
            content={
                "success": False,
                "message": "Access Token not found in the Cookies!",
            },
            status_code=401,
        )

    user_id = verify_access_token(token)

    return user_id
