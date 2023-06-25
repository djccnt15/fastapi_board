from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, validator

from .dto_common import no_empty_val, DateCreate, DateUpd
from .dto_user import User as UserRec, Id


class CategoryEnum(Enum):
    qna = 'qna'
    community = 'community'


class CategoryBase(BaseModel):
    category: str

    @validator('category')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v

    class Config:
        orm_mode = True


class CommentRec(Id[UUID], DateCreate):

    class Config:
        orm_mode = True


class ContentBase(BaseModel):
    content: str

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v


class CommentContent(ContentBase, DateUpd):

    class Config:
        orm_mode = True


class CommentDetail(BaseModel):
    Comment: CommentRec = Field(alias='comment')
    Content: CommentContent = Field(alias='content')
    User: UserRec = Field(alias='user')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostRec(Id[UUID], DateCreate):

    class Config:
        orm_mode = True


class SubjectBase(ContentBase):
    subject: str

    @validator('subject')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(no_empty_val)
        return v


class PostContent(SubjectBase, DateUpd):

    class Config:
        orm_mode = True


class PostSumm(BaseModel):
    Post: PostRec = Field(alias='post')
    Content: PostContent = Field(alias='content')
    Category: CategoryBase = Field(alias='category')
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
    Category: CategoryBase = Field(alias='category')
    User: UserRec = Field(alias='user')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostDetailList(BaseModel):
    post_detail: PostDetail
    comment_list: list[CommentDetail]

    class Config:
        allow_population_by_field_name = True


class PostCreate(SubjectBase, CategoryBase):
    ...