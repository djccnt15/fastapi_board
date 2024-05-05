from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger, Boolean, DateTime, Integer, String, Text

from .base_entity import BaseEntity
from .enum.post_enum import PostCategoryEntityEnum, PostContentEnum
from .user_entity import UserEntity


class PostCategoryEntity(BaseEntity):
    __tablename__ = "category"

    id = mapped_column(
        type_=BigInteger,
        primary_key=True,
        autoincrement=True,
        sort_order=-1,
    )  # need to override for relations
    tier = Column(
        Integer,
        nullable=False,
    )
    category = Column(
        String(length=PostCategoryEntityEnum.CATEGORY.value),
        nullable=False,
    )
    parent_id = Column(
        BigInteger,
        ForeignKey("category.id"),
    )

    parent = relationship(
        argument="PostCategoryEntity",
        remote_side=[id],
    )
    post = relationship(
        argument="PostEntity",
        back_populates="category",
    )


class PostEntity(BaseEntity):
    __tablename__ = "post"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        nullable=False,
    )

    category_id = Column(
        BigInteger,
        ForeignKey(PostCategoryEntity.id),
        nullable=False,
    )

    created_datetime = Column(
        DateTime,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    user = relationship(
        argument="UserEntity",
        back_populates="post",
    )
    category = relationship(
        argument="PostCategoryEntity",
        back_populates="post",
    )
    content = relationship(
        argument="PostContentEntity",
        back_populates="post",
    )
    comment = relationship(
        argument="CommentEntity",
        back_populates="post",
    )
    voter = relationship(
        argument="UserEntity",
        secondary="voter_post",
        back_populates="vote_post",
    )


class PostContentEntity(BaseEntity):
    __tablename__ = "post_content"

    id = Column(
        BigInteger,
        primary_key=True,
    )
    version = Column(
        Integer,
        nullable=False,
        default=0,
    )
    created_datetime = Column(
        DateTime,
        nullable=False,
    )
    subject = Column(
        String(length=PostContentEnum.SUBJECT.value),
        nullable=False,
    )
    content = Column(
        Text,
        nullable=False,
    )
    post_id = Column(
        BigInteger,
        ForeignKey(PostEntity.id),
        nullable=False,
    )

    post = relationship(
        argument="PostEntity",
        back_populates="content",
    )


class PostVoterEntity(BaseEntity):
    __tablename__ = "voter_post"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    psot_id = Column(
        BigInteger,
        ForeignKey(PostEntity.id),
        primary_key=True,
    )
