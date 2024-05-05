from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger, DateTime, String

from .base_entity import BaseEntity
from .enum.user_enum import (
    RoleEntityEnum,
    StateEntityEnum,
    UserEntityEnum,
    UserStateEntityEnum,
)


class UserEntity(BaseEntity):
    __tablename__ = "user"

    name = Column(
        String(length=UserEntityEnum.USERNAME.value),
        unique=True,
        index=True,
    )
    password = Column(
        String(length=UserEntityEnum.PASSWORDMAX.value),
    )
    email = Column(
        String(length=UserEntityEnum.EMAIL.value),
        unique=True,
        index=True,
    )
    created_datetime = Column(
        DateTime,
        nullable=False,
    )

    post = relationship(
        argument="PostEntity",
        back_populates="user",
    )
    comment = relationship(
        argument="CommentEntity",
        back_populates="user",
    )
    vote_post = relationship(
        argument="PostEntity",
        secondary="voter_post",
        back_populates="voter",
    )
    vote_comment = relationship(
        argument="CommentEntity",
        secondary="voter_comment",
        back_populates="voter",
    )
    role = relationship(
        argument="RoleEntity",
        secondary="user_role",
        back_populates="user",
    )
    user_state = relationship(
        argument="UserStateEntity",
        back_populates="user",
    )
    logged_in = relationship(
        argument="LoggedInEntity",
        back_populates="user",
    )


class RoleEntity(BaseEntity):
    __tablename__ = "role"

    name = Column(
        String(length=RoleEntityEnum.NAME.value),
        unique=True,
        nullable=False,
    )

    user = relationship(
        argument="UserEntity",
        secondary="user_role",
        back_populates="role",
    )


class UserRoleEntity(BaseEntity):
    __tablename__ = "user_role"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    role_id = Column(
        BigInteger,
        ForeignKey(RoleEntity.id),
        primary_key=True,
    )


class StateEntity(BaseEntity):
    __tablename__ = "state"

    name = Column(
        String(length=StateEntityEnum.NAME.value),
        unique=True,
        nullable=False,
    )

    user_state = relationship(
        argument="UserStateEntity",
        back_populates="state",
    )


class UserStateEntity(BaseEntity):
    __tablename__ = "user_state"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        primary_key=True,
    )
    state_id = Column(
        BigInteger,
        ForeignKey(StateEntity.id),
        primary_key=True,
    )
    detail = Column(String(length=UserStateEntityEnum.DETAIL.value))
    created_datetime = Column(
        DateTime,
        nullable=False,
    )

    user = relationship(
        argument="UserEntity",
        back_populates="user_state",
    )
    state = relationship(
        argument="StateEntity",
        back_populates="user_state",
    )


class LoggedInEntity(BaseEntity):
    __tablename__ = "logged_in"

    user_id = Column(
        BigInteger,
        ForeignKey(UserEntity.id),
        nullable=False,
    )
    created_datetime = Column(
        DateTime,
        nullable=False,
    )

    user = relationship(
        argument="UserEntity",
        back_populates="logged_in",
    )
