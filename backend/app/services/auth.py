import secrets
from uuid import uuid4
from datetime import timedelta, datetime
from app.core.email import render_template, send_email
from app.crud.auth import (
    get_token_by_user_id,
    get_user_by_email_or_username,
    create_token,
    get_token_by_code,
    delete_token,
    get_user_by_id,
    activate_user
)
from app.models.auth import TokenPurpose
from app.core.config import settings
from app.core.security import hash_password


RESET_TOKEN_EXPIRY_MINUTES = settings.RESET_PASSWORD_TOKEN_EXPIRY_MINUTES
EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = settings.EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS


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

    delete_token(session, token)
    return True


def verify_email_verification_token(token: str, session):
    verification_token = get_token_by_code(
        session, token, TokenPurpose.EMAIL_VERIFICATION
    )

    if not verification_token:
        return False

    #Expiry Check
    if datetime.utcnow() - verification_token.created_at > timedelta(
        hours=EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS
    ):
        delete_token(session, verification_token)
        return False

    user_id = verification_token.user_id

    activate_user(user_id, session)
    delete_token(session, verification_token)
    return True

def resend_verification_email(email: str, session):
    user = get_user_by_email_or_username(session, email)

    if not user:
        return {
            "success": False,
            "message": "No user found with the provided email!"
        }
    
    if user.email_verified:
        return {
            "success": False,
            "message": "This email is already verified, please login instead!"
        }

    token = get_token_by_user_id(user.id, session, TokenPurpose.EMAIL_VERIFICATION)

    if not token:
        token = create_token(session, user.id, uuid4().hex, TokenPurpose.EMAIL_VERIFICATION)

    return token
