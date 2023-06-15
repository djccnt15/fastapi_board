from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, Text, DateTime, Uuid
from sqlalchemy.orm import relationship

from settings.database import Base
from src.models.models import *
from src.models.post import *


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Uuid, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    id_post = Column(Uuid, ForeignKey(Post.id), nullable=False)
    date_create = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship('User', back_populates='comment')
    post = relationship('Post', back_populates='comment')
    content = relationship('CommentContent', back_populates='comment')


class CommentContent(Base):
    __tablename__ = 'comment_content'

    id = Column(Uuid, primary_key=True)
    version = Column(Integer, nullable=False)
    date_upd = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    id_comment = Column(Uuid, ForeignKey(Comment.id), nullable=False)

    comment = relationship('Comment', back_populates='content')