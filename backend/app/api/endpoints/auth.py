from uuid import uuid4

from fastapi import BackgroundTasks, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.api.dependencies import get_user
from app.core.security import (
    delete_auth_cookies,
    set_auth_cookies,
    set_reset_password_token_cookie,
    verify_password,
)
from app.core.token import (
    generate_access_token,
    generate_refresh_token,
    verify_refresh_token,
)
from app.crud.auth import (
    create_token,
    create_user,
    get_user_by_email_or_username,
    get_user_by_id,
)
from app.db.session import get_session
from app.models.auth import TokenPurpose
from app.models.user import User
from app.schemas.auth import (
    PerformPasswordReset,
    RequestPasswordReset,
    ValidateResetPasswordToken,
    VerifyEmail,
    ResendVerificationEmail,
)
from app.schemas.user import UserCreate
from app.services.auth import (
    generate_reset_token,
    reset_password,
    send_reset_password_email,
    send_verification_email,
    validate_reset_password_token,
    verify_email_verification_token,
    resend_verification_email,
)


def signup_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> JSONResponse:
    existing_user = get_user_by_email_or_username(
        session, user_in.email, user_in.username
    )
    if existing_user:
        return JSONResponse(
            content={"success": False, "message": "Email or Username already taken!"}
        )

    user = create_user(session, user_in)
    token = create_token(session, user.id, uuid4().hex, TokenPurpose.EMAIL_VERIFICATION)
    background_tasks.add_task(send_verification_email, user.email, token.code)

    return JSONResponse(
        {
            "success": True,
            "message": "Signup successful, please check your email for verification!",
        },
        status_code=201,
    )


def login_user(
    user_in: UserCreate, response: Response, session: Session = Depends(get_session)
) -> JSONResponse:
    user = get_user_by_email_or_username(session, user_in.email)

    if not user or not verify_password(user_in.password, user.hashed_password):
        return JSONResponse(
            content={"success": False, "message": "Invalid Credentials"},
            status_code=401,
        )

    if not user.is_verified():
        return JSONResponse(
            content={
                "success": False,
                "message": "Email Verification is pending, please verify and try again!",
            },
            status_code=403,
        )

    access_token = generate_access_token(user.id)
    refresh_token = generate_refresh_token(user.id)

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
            status_code=400,
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


def get_profile(session: Session = Depends(get_session), user_id=Depends(get_user)):
    if isinstance(user_id, JSONResponse):
        return user_id

    user: User = get_user_by_id(session=session, user_id=user_id)

    return JSONResponse(
        content={
            "success": True,
            "message": "User Profile Retrieved successfully!",
            "data": user.to_json(),
        },
        status_code=200,
    )


def request_reset_password(
    data: RequestPasswordReset, background_tasks: BackgroundTasks, session: Session
):
    code = generate_reset_token(session, data.email)
    if not code:
        raise HTTPException(status_code=404, detail="User not found")

    background_tasks.add_task(send_reset_password_email, data.email, code)

    return JSONResponse(
        content={"message": "Verification Link has been sent to your email address!"},
        status_code=200,
    )


def validate_reset_password_token_endpoint(
    request: Request, data: ValidateResetPasswordToken, session: Session
):
    token = data.code if data.code else request.cookies.get("reset_password_token")
    is_token_valid = validate_reset_password_token(token, session)

    if not is_token_valid:
        return JSONResponse(
            content={
                "success": False,
                "message": "The Link has Expired or is Invalid!",
            },
            status_code=400,
        )

    response = JSONResponse(
        content={
            "success": True,
            "message": "Your Password Reset request has been Validated!",
        },
        status_code=200,
    )

    set_reset_password_token_cookie(response, token)

    return response


def confirm_password_reset(
    request: Request, data: PerformPasswordReset, session: Session
):
    token = data.token if data.token else request.cookies.get("reset_password_token")
    success = reset_password(session, token, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return JSONResponse(
        content={"message": "Password reset successful"}, status_code=200
    )


def verify_email_endpoint(data: VerifyEmail, session: Session):
    token = data.token

    success = verify_email_verification_token(token, session)

    if not success:
        return JSONResponse(
            content={
                "success": False,
                "message": "The link is either Invalid or has Expired!",
            },
            status_code=400,
        )

    return JSONResponse(
        content={
            "success": True,
            "message": "Email verified successfully, you may now login!",
        }
    )


def resend_verification_email_endpoint(data: ResendVerificationEmail, background_tasks: BackgroundTasks, session: Session):
    email = data.email
    result = resend_verification_email(email, session)

    if isinstance(result, dict):
        return JSONResponse(content=result, status_code=400)

    background_tasks.add_task(send_verification_email, email, result.code)

    return JSONResponse(
        content={"success": True, "message": "Verification email sent successfully!"}
    )

def logout_endpoint():
    response = JSONResponse(content={
        "success": True,
        "message": "Logged out Successfully!"
    })

    delete_auth_cookies(response)

    return response
