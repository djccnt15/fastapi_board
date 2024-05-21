from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BigInteger, Boolean, DateTime, Integer, String, Text

from .base_entity import BaseEntity, BigintIdEntity
from .enum.post_enum import PostCategoryEntityEnum, PostContentEntityEnum
from .user_entity import UserEntity


class PostCategoryEntity(BigintIdEntity):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        type_=BigInteger,
        primary_key=True,
        autoincrement=True,
        sort_order=-1,
    )  # need to override for self relations
    tier: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(length=PostCategoryEntityEnum.CATEGORY.value),
        nullable=False,
    )
    parent_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("category.id"),
    )

    parent = relationship(
        argument="PostCategoryEntity",
        remote_side=[id],
    )


class PostEntity(BigintIdEntity):
    __tablename__ = "post"

    user_id: Mapped["UserEntity"] = mapped_column(
        BigInteger,
        ForeignKey(UserEntity.id),
        nullable=False,
    )
    category_id: Mapped["PostCategoryEntity"] = mapped_column(
        BigInteger,
        ForeignKey(PostCategoryEntity.id),
        nullable=False,
    )
    created_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    user = relationship(
        argument="UserEntity",
        back_populates="post",
        lazy="selectin",
    )


class PostContentEntity(BigintIdEntity):
    __tablename__ = "post_content"

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    created_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(length=PostContentEntityEnum.TITLE.value),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    post_id: Mapped["PostEntity"] = mapped_column(
        BigInteger,
        ForeignKey(PostEntity.id),
        nullable=False,
    )


class PostVoterEntity(BaseEntity):
    __tablename__ = "voter_post"

    user_id: Mapped["UserEntity"] = mapped_column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    post_id: Mapped["PostEntity"] = mapped_column(
        BigInteger,
        ForeignKey(PostEntity.id),
        primary_key=True,
    )
