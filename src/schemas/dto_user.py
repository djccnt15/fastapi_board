from pydantic import BaseModel, EmailStr, validator, Field

from .dto_common import no_empty_val, Id

conflict_email = 'email conflict'
conflict_username = 'user name conflict'


class UserName(BaseModel):
    username: str = Field(max_length=50)


class UserEmail(BaseModel):
    email: EmailStr


class UserCreate(UserName, UserEmail):
    password1: str = Field(max_length=100, min_length=8)
    password2: str = Field(max_length=100, min_length=8)

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('password1 and password2 are not equal')
        return v


class User(Id[int], UserName):
    is_superuser: bool | None = None
    is_staff: bool | None = None
    is_blocked: bool | None = None
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str