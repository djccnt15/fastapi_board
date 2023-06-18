from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator

from src.schemas.common.user import User
from src.schemas.common.category import Category
from src.schemas.common.common import no_empty_val
from src.schemas.board.comment import CommentDetail


class Post(BaseModel):
    id: UUID
    date_create: datetime

    class Config:
        orm_mode = True


class PostContent(BaseModel):
    id: UUID
    date_upd: datetime
    subject: str
    content: str

    class Config:
        orm_mode = True


class PostSumm(BaseModel):
    Post: Post
    Content: PostContent
    Category: Category
    User: User

    class Config:
        orm_mode = True


class PostList(BaseModel):
    total: int
    post_list: list[PostSumm]


class PostDetail(BaseModel):
    Post: Post
    Content: PostContent
    Category: Category
    User: User

    class Config:
        orm_mode = True


class PostDetailList(BaseModel):
    post: PostDetail
    comment: list[CommentDetail]


class PostCreate(BaseModel):
    category: str
    subject: str
    content: str

    @validator('category', 'subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v