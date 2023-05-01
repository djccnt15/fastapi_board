from datetime import datetime

from pydantic import BaseModel

from src.schemas.common.user import User
from src.schemas.common.category import Category
from src.schemas.board.comment import Comment


class PostSumm(Category):
    id: int
    date_create: datetime
    subject: str
    username: str

    class Config:
        orm_mode = True


class PostList(BaseModel):
    total: int = 0
    post_list: list[PostSumm] = []


class Post(BaseModel):
    id: int
    date_create: datetime
    category: Category
    user: User

    class Config:
        orm_mode = True


class PostContent(BaseModel):
    version: int
    date_upd: datetime
    subject: str
    content: str

    class Config:
        orm_mode = True


class PostDetail(BaseModel):
    post: Post
    content: PostContent
    comment: list[Comment] = []