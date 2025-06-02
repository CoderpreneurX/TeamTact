from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Invitation(SQLModel, table=True):
    __tablename__ = "invitations"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    team_id: UUID = Field(foreign_key="teams.id")
    email: str = Field(index=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    token: str = Field(default_factory=lambda: uuid4().hex, unique=True, index=True)
    invited_at: datetime = Field(default_factory=datetime.utcnow)
    expiration_date: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=3)
    )
    is_cancelled: bool = Field(default=False)
    is_accepted: bool = Field(default=False)
    accepted_at: Optional[datetime] = None

    team: Optional["Team"] = Relationship(back_populates="invitations")

    def to_json(self):
        return {
            "id": str(self.id),
            "team_id": str(self.team_id),
            "email": self.email,
            "user_id": self.user_id,
            "token": self.token,
            "invited_at": self.invited_at.isoformat(),
            "expiration_date": self.expiration_date.isoformat(),
            "is_cancelled": self.is_cancelled,
            "is_accepted": self.is_accepted,
            "team": self.team.to_json(),
        }


class TeamMate(SQLModel, table=True):
    __tablename__ = "team_mates"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    team_id: UUID = Field(foreign_key="teams.id")
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")

    joined_at: datetime = Field(default_factory=datetime.utcnow)

    team: Optional["Team"] = Relationship(back_populates="members")

    user: Optional["User"] = Relationship(back_populates="teammate")

    def to_json(self):
        return {
            "id": str(self.id),
            "team_id": str(self.team_id),
            "user_id": str(self.user_id),
            "joined_at": self.joined_at.isoformat(),
            "team": self.team.to_json(),
        }


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    code: str
    owner_id: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    members: List[TeamMate] = Relationship(back_populates="team")
    invitations: List[Invitation] = Relationship(back_populates="team")

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "owner_id": str(self.owner_id),
            "created_at": self.created_at.isoformat(),
            "members": [member.to_json() for member in self.members],
            "invitations": [invitation.to_json() for invitation in self.invitations],
        }
