from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


def get_user_by_email_or_username(session: Session, email: str, username: str):
    statement = select(User).where((User.email == email) | (User.username == username))
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
