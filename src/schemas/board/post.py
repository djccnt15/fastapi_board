from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    id: int
    date_create: datetime
    subject: str
    category: str
    user: str

    class Config:
        orm_mode = True


class PostList(BaseModel):
    total: int = 0
    post_list: list[Post] = []