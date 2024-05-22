from pydantic import BaseModel, Field, ValidationInfo, field_validator

from src.common.exception import WhiteSpaceError
from src.db.entity.enum.post_enum import PostCategoryEntityEnum, PostContentEntityEnum
from src.domain.board.model.enums import board_enum


class PostBaseRequset(BaseModel):
    title: str = Field(max_length=PostContentEntityEnum.TITLE)
    content: str = Field(max_length=PostContentEntityEnum.CONTENT)

    @field_validator("title", "content")
    @classmethod
    def check_empty(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise WhiteSpaceError(field=info.field_name)
        return v


class PostUpdateRequest(PostBaseRequset):
    category: board_enum.CategoryEnum = Field(
        max_length=PostCategoryEntityEnum.CATEGORY
    )
