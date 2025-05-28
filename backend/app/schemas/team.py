from pydantic import BaseModel, EmailStr
from typing import List
from uuid import UUID


class TeamCreate(BaseModel):
    name: str


class TeamRead(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class InviteRequest(BaseModel):
    emails: List[EmailStr]
