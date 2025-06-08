import secrets
from datetime import timedelta, datetime
from app.core.email import render_template, send_email
from app.crud.auth import (
    get_user_by_email_or_username,
    create_token,
    get_token_by_code,
    delete_token,
    get_user_by_id,
)
from app.models.auth import TokenPurpose
from app.core.config import settings
from app.core.security import hash_password


RESET_TOKEN_EXPIRY_MINUTES = settings.AUTH_TOKEN_EXPIRY_MINUTES


def send_verification_email(to_email: str, token_code: str):
    verify_link = f"{settings.FRONTEND_DOMAIN}verify-email?token={token_code}"

    html_body = render_template("verify_email.html", verify_link=verify_link)

    subject = "[TeamTact] Verify your email address"
    send_email(subject=subject, to_email=to_email, html_body=html_body)


def send_reset_password_email(to_email: str, token_code: str):
    reset_link = f"{settings.FRONTEND_DOMAIN}reset-password?token={token_code}"

    html_body = render_template("password_reset.html", reset_link=reset_link)

    subject = "[TeamTact] Reset your password"
    send_email(subject=subject, to_email=to_email, html_body=html_body)


def generate_reset_token(session, email: str) -> str:
    user = get_user_by_email_or_username(session, email=email)
    if not user:
        return None
    code = secrets.token_urlsafe(32)
    create_token(
        session, user_id=user.id, code=code, purpose=TokenPurpose.RESET_PASSWORD
    )
    return code


def reset_password(session, code: str, new_password: str) -> bool:
    token = get_token_by_code(session, code=code, purpose=TokenPurpose.RESET_PASSWORD)
    if not token:
        return False

    # Expiry check
    if datetime.utcnow() - token.created_at > timedelta(
        minutes=RESET_TOKEN_EXPIRY_MINUTES
    ):
        delete_token(session, token)
        return False

    user = get_user_by_id(session, token.user_id)
    if not user:
        return False

    user.hashed_password = hash_password(new_password)
    delete_token(session, token)
    session.add(user)
    session.commit()
    return True

def validate_reset_password_token(code, session):
    token = get_token_by_code(session, code=code, purpose=TokenPurpose.RESET_PASSWORD)

    if not token:
        return False

    # Expiry check
    if datetime.utcnow() - token.created_at > timedelta(
        minutes=RESET_TOKEN_EXPIRY_MINUTES
    ):
        delete_token(session, token)
        return False
    
    user = get_user_by_id(session, token.user_id)
    if not user:
        return False
    
    return True
