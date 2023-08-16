from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, DateTime, Uuid
from sqlalchemy.orm import relationship

from common.database import Base


class Log(Base):
    __tablename__ = 'log'

    id = Column(Uuid, primary_key=True)
    date_create = Column(DateTime, nullable=False)
    log = Column(Text, nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    date_create = Column(DateTime, nullable=False)

    post = relationship('Post', back_populates='user')
    comment = relationship('Comment', back_populates='user')
    vote_post = relationship('Post', secondary='voter_post', back_populates='voter')
    vote_comment = relationship('Comment', secondary='voter_comment', back_populates='voter')
    role = relationship('Role', secondary='user_role', back_populates='user')
    logged_in = relationship('LoggedIn', back_populates='user')


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True, nullable=False)

    user = relationship('User', secondary='user_role', back_populates='role')


class UserRole(Base):
    __tablename__ = 'user_role'

    id_user = Column(Integer, ForeignKey(User.id), primary_key=True)
    id_role = Column(Integer, ForeignKey(Role.id), primary_key=True)


class LoggedIn(Base):
    __tablename__ = 'logged_in'

    id = Column(Uuid, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    date_create = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='logged_in')