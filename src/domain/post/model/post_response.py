from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.core.model.common_model import IdModel


class PostResponse(IdModel[int]):
    created_datetime: datetime
    updated_datetime: datetime
    category: str
    user: str
    title: str
    content: str


class BoardPostResponse(PostResponse):
    comment: int | None
    vote: int | None


class PostContentResponse(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        from_attributes=True,
    )

    version: int
    created_datetime: datetime = Field(serialization_alias="updated_datetime")
    title: str
    content: str
