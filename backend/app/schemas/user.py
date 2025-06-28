from sqlmodel import SQLModel
from uuid import UUID


class UserCreate(SQLModel):
    fullname: str
    email: str
    username: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: UUID
    fullname: str
    email: str
    username: str
