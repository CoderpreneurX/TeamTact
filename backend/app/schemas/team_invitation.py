from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.team import TeamMateRole
from app.schemas.user import UserRead


class InvitationResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: TeamMateRole
    invitor: UserRead
    invited_at: datetime

    class Config:
        from_attributes = True


class InvitationData(BaseModel):
    email: EmailStr
    role: TeamMateRole


class InvitationCreateRequest(BaseModel):
    invitations: List[InvitationData]
