from typing import Iterable

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from src.common.exception import WhiteSpaceError
from src.domain.post.model import post_response


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

    @field_validator("name")
    def check_empty(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise WhiteSpaceError(field=info.field_name)
        return v


class PostListResponse(BaseModel):
    total: int
    post_list: Iterable[post_response.BoardPostResponse]
