from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class TeamCreateRequest(BaseModel):
    name: str


class TeamResponse(BaseModel):
    id: UUID
    name: str
    code: str
    owner_id: UUID
    created_at: datetime
    members_count: int

    class Config:
        from_attributes = True
