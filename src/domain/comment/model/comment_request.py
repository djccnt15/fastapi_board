from pydantic import BaseModel, Field, ValidationInfo, field_validator

from src.core.exception import WhiteSpaceError
from src.db.entity.enum.comment_enum import CommentContentEntityEnum


class CommentCreateRequest(BaseModel):
    content: str = Field(max_length=CommentContentEntityEnum.CONTENT)

    @field_validator("content")
    @classmethod
    def check_empty(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise WhiteSpaceError(field=info.field_name)
        return v
