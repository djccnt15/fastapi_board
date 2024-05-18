from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.common.model.common_model import IdModel


class CommentResponse(IdModel[int]):
    created_datetime: datetime
    updated_datetime: datetime
    user: str
    content: str
    vote: int | None


class CommentContentResponse(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        from_attributes=True,
    )

    version: int
    created_datetime: datetime = Field(serialization_alias="updated_datetime")
    content: str
