import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, UniqueConstraint, Relationship
from uuid import UUID


class UserBase(SQLModel):
    fullname: str
    email: str = Field(index=True, nullable=False)
    username: str = Field(index=True, nullable=False)
    is_active: bool = True
    email_verified: bool = False


class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email"),
        UniqueConstraint("username"),
    )

    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    teammate: Optional["TeamMate"] = Relationship(back_populates="user")

    def is_verified(self) -> bool:
        return self.email_verified

    def to_json(self) -> dict:
        return {
            "id": str(self.id),
            "fullname": self.fullname,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
