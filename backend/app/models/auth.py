from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from enum import Enum


class TokenPurpose(str, Enum):
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"


class Token(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    code: str = Field(index=True, unique=True)
    purpose: TokenPurpose
    created_at: datetime = Field(default_factory=datetime.utcnow)
