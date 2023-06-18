from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator

from src.schemas.common.user import User
from src.schemas.common.common import no_empty_val

class Comment(BaseModel):
    id: UUID
    date_create: datetime

    class Config:
        orm_mode = True


class CommentContent(BaseModel):
    id: UUID
    date_upd: datetime
    content: str

    class Config:
        orm_mode = True


class CommentDetail(BaseModel):
    Comment: Comment
    Content: CommentContent
    User: User

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v