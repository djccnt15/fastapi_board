from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from src.core.exception import AlphanumericError, PasswordNotMatchError, WhiteSpaceError
from src.core.model.common import IdModel
from src.db.entity.enum.user_enum import UserEntityEnum


class UserBase(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    name: str = Field(max_length=UserEntityEnum.NAME)
    email: EmailStr = Field(max_length=UserEntityEnum.EMAIL)

    @field_validator("name", "email")
    @classmethod
    def check_whitespace(cls, v: str, info: ValidationInfo) -> str:
        condition = any([not v, not v.strip(), v != v.replace(" ", "")])
        if condition:
            raise WhiteSpaceError(field=info.field_name)
        return v

    @field_validator("name")
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        if not v.isalnum():
            raise AlphanumericError(field=info.field_name)
        return v


class Password(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

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
            raise PasswordNotMatchError
        return self


class UserCreateRequest(Password, UserBase): ...


class UserCurrent(IdModel[int], UserBase):
    model_config = ConfigDict(from_attributes=True)
