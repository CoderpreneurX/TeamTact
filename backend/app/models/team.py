"""
This module defines the SQLModel classes for managing teams, team members, and invitations.

It includes:
- `Invitation`: Represents an invitation for a user to join a team.
- `TeamMate`: Represents a user's membership within a team, including their role.
- `Team`:
    Represents a team, including its: name, code, owner, and associated members and invitations.
"""

from datetime import datetime, timedelta
from enum import Enum as PyEnum
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel, Index, func

from app.models.user import User


class TeamMateRole(str, PyEnum):
    """
    Enum that includes the roles for the teammates.

    Attributes:
        OWNER (str): The Owner's Role (Full Control)
        ADMIN (str): The Admin's Role (Manage Teams and Teammates)
        VIEWER (str): The Viewer's Role (View Teams and Teammates)
    """

    OWNER = "OWNER"
    ADMIN = "ADMIN"
    VIEWER = "VIEWER"


class Invitation(SQLModel, table=True):
    """
    Represents an invitation for a user to join a team.

    Attributes:
        id (UUID): Unique identifier for the invitation.
        team_id (UUID):
            Foreign key to the `Team` table, indicating the team being invited to.
        email (str): The email address of the invited user.
        invited_by (UUID): Foreign key to the `User` table, indicating who sent the invitation.
        token (str): A unique token used for accepting the invitation.
        invited_at (datetime): The timestamp when the invitation was sent.
        expiration_date (datetime): The timestamp when the invitation expires.
        is_cancelled (bool): True if the invitation has been cancelled, False otherwise.
        is_accepted (bool): True if the invitation has been accepted, False otherwise.
        accepted_at (Optional[datetime]):
            The timestamp when the invitation was accepted, if applicable.
        team (Optional[Team]): The related Team object.
    """

    __tablename__ = "invitations"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    team_id: UUID = Field(foreign_key="teams.id")
    email: str = Field(index=True)
    role: TeamMateRole = Field(default=TeamMateRole.VIEWER, index=True)
    invited_by: UUID = Field(foreign_key="users.id", index=True)  # NEW
    token: str = Field(default_factory=lambda: uuid4().hex, unique=True, index=True)
    invited_at: datetime = Field(default_factory=datetime.utcnow)
    expiration_date: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=3)
    )
    is_cancelled: bool = Field(default=False)
    is_accepted: bool = Field(default=False)
    accepted_at: Optional[datetime] = None

    invitor: Optional["User"] = Relationship(back_populates="invitations")
    team: Optional["Team"] = Relationship(back_populates="invitations")


class TeamMate(SQLModel, table=True):
    """
    Represents a user's membership within a team.

    Attributes:
        id (UUID): Unique identifier for the team membership.
        team_id (UUID): Foreign key to the `Team` table.
        user_id (Optional[UUID]):
            Foreign key to the `User` table, if the member is a registered user.
        role (TeamMateRole):
            The role of the user within the team (e.g., 'viewer', 'admin', 'owner').
        joined_at (datetime): The timestamp when the user joined the team.
        team (Optional[Team]): The related Team object.
        user (Optional[User]): The related User object.
    """

    __tablename__ = "team_mates"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    team_id: UUID = Field(foreign_key="teams.id")
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    role: TeamMateRole = Field(default=TeamMateRole.VIEWER, index=True)

    joined_at: datetime = Field(default_factory=datetime.utcnow)

    team: Optional["Team"] = Relationship(back_populates="members")
    user: Optional["User"] = Relationship(back_populates="teammate")


class Team(SQLModel, table=True):
    """
    Represents a team in the system.

    Attributes:
        id (UUID): Unique identifier for the team.
        name (str): The name of the team.
        code (str): A unique code associated with the team.
        owner_id (UUID): Foreign key to the `User` table, indicating the owner of the team.
        created_at (datetime): The timestamp when the team was created.
        members (List[TeamMate]): A list of TeamMate objects associated with this team.
        invitations (List[Invitation]): A list of Invitation objects associated with this team.
    """

    __tablename__ = "teams"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    code: str = Field(index=True)
    owner_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    members: List[TeamMate] = Relationship(back_populates="team")
    invitations: List[Invitation] = Relationship(back_populates="team")

    @property
    def members_count(self) -> int:
        return len(self.members)

Index(
    "uq_owner_team_name_insensitive",
    Team.__table__.c.owner_id, # type: ignore
    func.lower(Team.__table__.c.name), # type: ignore
    unique=True
)