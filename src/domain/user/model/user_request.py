from typing import Self

from fastapi import HTTPException
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)
from starlette import status

from src.core.exception import WhiteSpaceError
from src.core.model import IdModel
from src.db.entity.enum.user_enum import UserEntityEnum


class UserBase(BaseModel):
    name: str = Field(max_length=UserEntityEnum.NAME)
    email: EmailStr = Field(max_length=UserEntityEnum.EMAIL)

    @field_validator("name")
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        if not v.encode().isalnum():
            # used encode method here to make korean returns false
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{info.field_name} must be alphanumeric",
            )
        return v


class Password(BaseModel):
    password1: str = Field(
        max_length=UserEntityEnum.PASSWORDMAX,
        min_length=UserEntityEnum.PASSWORDMIN,
    )
    password2: str = Field(
        max_length=UserEntityEnum.PASSWORDMAX,
        min_length=UserEntityEnum.PASSWORDMIN,
    )

    @field_validator("password1", "password2")
    @classmethod
    def check_whitespace(cls, v: str, info: ValidationInfo) -> str:
        condition = any([not v, not v.strip(), v != v.replace(" ", "")])
        if condition:
            raise WhiteSpaceError(field=info.field_name)
        return v

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        pw1 = self.password1
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password1 and password2 are not equal",
            )
        return self


class UserCreateRequest(Password, UserBase): ...


class UserCurrent(IdModel[int], UserBase):
    model_config = ConfigDict(from_attributes=True)
