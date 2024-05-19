from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import BigInteger, DateTime, String

from .base_entity import BaseEntity, BigintIdEntity
from .enum.user_enum import (
    RoleEntityEnum,
    StateEntityEnum,
    UserEntityEnum,
    UserStateEntityEnum,
)


class UserEntity(BigintIdEntity):
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
    state = relationship(
        argument="StateEntity",
        secondary="user_state",
        back_populates="user",
        lazy="selectin",
    )


class RoleEntity(BigintIdEntity):
    __tablename__ = "role"

    name = Column(
        String(length=RoleEntityEnum.NAME.value),
        unique=True,
        nullable=False,
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


class StateEntity(BigintIdEntity):
    __tablename__ = "state"

    name = Column(
        String(length=StateEntityEnum.NAME.value),
        unique=True,
        nullable=False,
    )

    user = relationship(
        argument="UserEntity",
        secondary="user_state",
        back_populates="state",
        lazy="selectin",
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


class LoggedInEntity(BigintIdEntity):
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
