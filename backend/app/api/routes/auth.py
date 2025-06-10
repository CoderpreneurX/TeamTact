from fastapi import APIRouter, BackgroundTasks, Request, Response, Depends
from app.api.dependencies import get_user
from app.api.endpoints.auth import (
    confirm_password_reset,
    get_profile,
    refresh_access_token,
    request_reset_password,
    signup_user,
    login_user,
    validate_reset_password_token_endpoint,
    verify_email_endpoint,
    resend_verification_email_endpoint,
)
from app.schemas.auth import (
    PerformPasswordReset,
    RequestPasswordReset,
    ValidateResetPasswordToken,
    VerifyEmail,
    ResendVerificationEmail,
)
from app.schemas.user import UserCreate, UserRead, UserLogin
from sqlmodel import Session
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


@router.post("/signup", response_model=UserRead)
def signup_route(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    return signup_user(user_in, background_tasks, session)


@router.post("/login", response_model=UserRead)
def login_route(
    user_in: UserLogin, response: Response, session: Session = Depends(get_session)
):
    return login_user(user_in, response, session)


@router.get("/refresh")
def refresh_access_token_route(request: Request):
    return refresh_access_token(request)


@router.get("/me")
def get_profile_route(
    session: Session = Depends(get_session), user_id: str = Depends(get_user)
):
    return get_profile(session=session, user_id=user_id)


@router.post("/request-reset-password")
def request_password_reset_route(
    data: RequestPasswordReset,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    return request_reset_password(data, background_tasks, session)


@router.post("/confirm-reset-password")
def confirm_password_reset_route(
    request: Request,
    data: PerformPasswordReset,
    session: Session = Depends(get_session),
):
    return confirm_password_reset(request, data, session)


@router.post("/validate-reset-password-token")
def validate_reset_password_token_route(
    request: Request,
    data: ValidateResetPasswordToken,
    session: Session = Depends(get_session),
):
    return validate_reset_password_token_endpoint(request, data, session)


@router.post("/verify-email")
def verify_email_route(data: VerifyEmail, session: Session = Depends(get_session)):
    return verify_email_endpoint(data, session)


@router.post("/resend-verification-email")
def resend_verification_email_route(
    data: ResendVerificationEmail, background_tasks: BackgroundTasks, session: Session = Depends(get_session)
):
    return resend_verification_email_endpoint(data, background_tasks, session)
