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


class Category(CategoryBase):
    category_t1: str


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


class CommentBase(BaseModel):
    Comment: CommentRec = Field(alias='comment')
    content: CommentContent


class CommentDetail(CommentBase):
    User: UserRec = Field(alias='user')
    count_vote: int | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostRec(Id[UUID], DateCreate):

    class Config:
        orm_mode = True


class CommentSumm(CommentBase):
    Post: PostRec = Field(alias='post')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


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


class PostSumm(Category):
    Post: PostRec = Field(alias='post')
    content: PostContent
    User: UserRec = Field(alias='user')
    count_comment: int | None
    count_vote: int | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostList(BaseModel):
    total: int
    post_list: list[PostSumm]


class PostDetailBase(Category):
    Post: PostRec = Field(alias='post')
    content: PostContent
    User: UserRec = Field(alias='user')
    count_vote: int | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PostDetail(BaseModel):
    post_detail: PostDetailBase
    comment_list: list[CommentDetail]


class PostCreate(SubjectBase, CategoryBase):
    ...


class PostHis(BaseModel):
    post_his: list[PostContent]


class CommentHis(BaseModel):
    comment_his: list[CommentContent]