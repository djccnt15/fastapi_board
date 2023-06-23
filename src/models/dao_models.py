from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Integer, String, Text, DateTime, Uuid
from sqlalchemy.orm import relationship

from settings.database import Base


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
    is_superuser = Column(Boolean, default=None)
    is_staff = Column(Boolean, default=None)
    is_blocked = Column(Boolean, default=None)
    is_active = Column(Boolean, nullable=False, default=True)

    post = relationship('Post', back_populates='user')
    comment = relationship('Comment', back_populates='user')