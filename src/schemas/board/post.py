from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from src.schemas.common.user import User
from src.schemas.common.category import Category
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
    total: int = 0
    post_list: list[PostSumm] = []


class PostDetail(BaseModel):
    Post: Post
    Content: PostContent
    Category: Category
    User: User

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    post: PostDetail
    comment: list[CommentDetail]

    class Config:
        orm_mode = True