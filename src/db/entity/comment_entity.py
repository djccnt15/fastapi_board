from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BigInteger, Boolean, DateTime, Integer, Text

from .base_entity import BaseEntity, BigintIdEntity
from .post_entity import PostEntity
from .user_entity import UserEntity


class CommentEntity(BigintIdEntity):
    __tablename__ = "comment"

    user_id: Mapped["UserEntity"] = mapped_column(
        BigInteger,
        ForeignKey(UserEntity.id),
        nullable=False,
    )
    post_id: Mapped["PostEntity"] = mapped_column(
        BigInteger,
        ForeignKey(PostEntity.id),
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
        back_populates="comment",
        lazy="selectin",
    )


class CommentContentEntity(BigintIdEntity):
    __tablename__ = "comment_content"

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    created_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    comment_id: Mapped["CommentEntity"] = mapped_column(
        BigInteger,
        ForeignKey(CommentEntity.id),
        nullable=False,
    )


class CommentVoterEntity(BaseEntity):
    __tablename__ = "voter_comment"

    user_id: Mapped["UserEntity"] = mapped_column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    comment_id: Mapped["CommentEntity"] = mapped_column(
        BigInteger,
        ForeignKey(CommentEntity.id),
        primary_key=True,
    )
