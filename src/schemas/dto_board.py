from uuid import UUID
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, validator

from .dto_common import no_empty_val
from .dto_user import User as UserRec, Id


class CategoryEnum(Enum):
    qna = 'qna'
    community = 'community'


class CategoryRec(BaseModel):
    category: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CommentRec(Id[UUID]):
    date_create: datetime

    class Config:
        orm_mode = True


class CommentContent(Id[UUID]):
    date_upd: datetime
    content: str

    class Config:
        orm_mode = True


class CommentDetail(BaseModel):
    Comment: CommentRec = Field(alias='comment')
    Content: CommentContent = Field(alias='content')
    User: UserRec = Field(alias='user')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CommentCreate(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v


class PostRec(BaseModel):
    id: UUID
    date_create: datetime

    class Config:
        orm_mode = True


class PostContentBase(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v


class PostContent(Id[UUID], PostContentBase):
    date_upd: datetime

    class Config:
        orm_mode = True


class PostSumm(BaseModel):
    Post: PostRec = Field(alias='post')
    Content: PostContent = Field(alias='content')
    Category: CategoryRec = Field(alias='category')
    User: UserRec = Field(alias='user')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostList(BaseModel):
    total: int
    post_list: list[PostSumm]


class PostDetail(BaseModel):
    Post: PostRec = Field(alias='post')
    Content: PostContent = Field(alias='content')
    Category: CategoryRec = Field(alias='category')
    User: UserRec = Field(alias='user')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostDetailList(BaseModel):
    post_detail: PostDetail
    comment_list: list[CommentDetail]

    class Config:
        allow_population_by_field_name = True


class PostCreate(BaseModel):
    category: str
    subject: str
    content: str

    @validator('category', 'subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v