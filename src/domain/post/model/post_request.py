from pydantic import BaseModel, ValidationInfo, field_validator

from src.common.exception import WhiteSpaceError
from src.domain.board.model.enums import board_enum


class PostBaseRequset(BaseModel):
    title: str
    content: str

    @field_validator("title", "content")
    @classmethod
    def check_empty(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise WhiteSpaceError(field=info.field_name)
        return v


class PostCreateRequest(PostBaseRequset):
    category: board_enum.CategoryEnum
