from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4


class TeamMate(SQLModel, table=True):
    __tablename__ = "team_mates"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    team_id: UUID = Field(foreign_key="teams.id")
    email: str = Field(index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    invite_token: str = Field(default_factory=lambda: uuid4().hex, unique=True, index=True)
    joined: bool = Field(default=False)
    invited_at: datetime = Field(default_factory=datetime.utcnow)
    joined_at: Optional[datetime] = None
    cancelled: bool = Field(default=False)

    team: Optional["Team"] = Relationship(back_populates="members")


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    owner_id: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    members: List[TeamMate] = Relationship(back_populates="team")
