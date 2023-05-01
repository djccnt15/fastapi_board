from datetime import date

from pydantic import BaseModel, EmailStr, validator


class UserName(BaseModel):
    username: str


class UserEmail(BaseModel):
    email: EmailStr


class UserCreate(UserName, UserEmail):
    password1: str
    password2: str

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('empty space is not allowed for password')
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('password1 and password2 are not equal')
        return v


class User(UserName):
    is_superuser: bool | None = None
    is_staff: bool | None = None
    is_blocked: bool | None = None
    is_active: bool

    class Config:
        orm_mode = True


class UserInfo(User, UserEmail):
    id: int
    date_create: date