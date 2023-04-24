from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    date_create: datetime


class User(UserBase):
    id: int
    is_superuser: bool
    is_staff: bool

    class Config:
        orm_mode = True