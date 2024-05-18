from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from src.common.exception import WhiteSpaceError


class CommentBaseRequest(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    content: str

    @field_validator("content")
    @classmethod
    def check_empty(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise WhiteSpaceError(field=info.field_name)
        return v


class CommentCreateRequest(CommentBaseRequest):
    post_id: int
