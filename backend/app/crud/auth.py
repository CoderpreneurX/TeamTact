"""
This module handles the CRUD related to Authentication
"""

from typing import Optional

from sqlmodel import Session, or_, select

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email_or_username(
    session: Session, email: str, username: Optional[str] = None
):
    """
    Returns a User based on the provided username or email
    """
    if username:
        statement = select(User).where(
            or_(User.email == email, User.username == username)
        )
    else:
        statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: str):
    """
    Returns the User based on the user_id provided
    """
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def create_user(session: Session, user_in: UserCreate) -> User:
    """
    Creates a User based on the credentials provided
    """
    user = User(
        fullname=user_in.fullname,
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
