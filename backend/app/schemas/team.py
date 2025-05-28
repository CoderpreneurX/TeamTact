from pydantic import BaseModel
from pydantic import ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List


# Shallow team representation to avoid recursion
class TeamSimpleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class InvitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    team_id: UUID
    email: str
    user_id: Optional[UUID]
    token: str
    invited_at: datetime
    expiration_date: datetime
    is_cancelled: bool
    is_accepted: bool
    accepted_at: Optional[datetime]
    team: Optional[TeamSimpleRead]


class TeamMateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    team_id: UUID
    user_id: Optional[UUID]
    joined_at: datetime
    team: Optional[TeamSimpleRead]


class TeamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    owner_id: UUID
    created_at: datetime
    members: List[TeamMateRead] = []
    invitations: List[InvitationRead] = []
