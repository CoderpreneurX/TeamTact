from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.team import TeamMateRole
from app.schemas.user import UserRead


class TeamMateResponse(BaseModel):
    id: UUID
    user: UserRead
    role: TeamMateRole
    joined_at: datetime

    class Config:
        from_attributes = True


class TeamMateListQuery(BaseModel):
    search: Optional[str] = None
    role: Optional[TeamMateRole] = None
    page: int = 1
    per_page: int = 10
