from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger, Boolean, DateTime, Integer, Text

from .base_entity import BaseEntity, BigintIdEntity
from .post_entity import PostEntity
from .user_entity import UserEntity


class CommentEntity(BigintIdEntity):
    __tablename__ = "comment"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        nullable=False,
    )
    post_id = Column(
        BigInteger,
        ForeignKey(PostEntity.id),
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
        back_populates="comment",
        lazy="selectin",
    )


class CommentContentEntity(BigintIdEntity):
    __tablename__ = "comment_content"

    version = Column(
        Integer,
        nullable=False,
        default=0,
    )
    created_datetime = Column(
        DateTime,
        nullable=False,
    )
    content = Column(
        Text,
        nullable=False,
    )
    comment_id = Column(
        BigInteger,
        ForeignKey(CommentEntity.id),
        nullable=False,
    )


class CommentVoterEntity(BaseEntity):
    __tablename__ = "voter_comment"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    comment_id = Column(
        BigInteger,
        ForeignKey(CommentEntity.id),
        primary_key=True,
    )
