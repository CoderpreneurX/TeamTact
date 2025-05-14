from sqlmodel import Session, select, or_
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from typing import Optional


def get_user_by_email_or_username(
    session: Session, email: str, username: Optional[str] = None
):
    if username:
        statement = select(User).where(
            or_(User.email == email, User.username == username)
        )
    else:
        statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, user_in: UserCreate) -> User:
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
