from sqlmodel import SQLModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserCreate(SQLModel):
    fullname: str
    email: str
    username: str
    password: str


class UserRead(SQLModel):
    id: UUID
    fullname: str
    email: str
    username: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime
