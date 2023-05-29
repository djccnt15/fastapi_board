from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from src.schemas.common.user import User

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