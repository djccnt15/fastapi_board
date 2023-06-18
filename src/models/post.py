from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, Text, DateTime, Uuid
from sqlalchemy.orm import relationship

from settings.database import Base
from src.models.models import *


class PostCategory(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    tier = Column(Integer, nullable=False)
    category = Column(String(length=255), nullable=False)
    id_parent = Column(Integer, ForeignKey('category.id'))

    parent = relationship(argument='PostCategory', remote_side=[id])
    post = relationship('Post', back_populates='category')


class Post(Base):
    __tablename__ = 'post'

    id = Column(Uuid, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    id_category = Column(Integer, ForeignKey(PostCategory.id), nullable=False)
    date_create = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    user = relationship('User', back_populates='post')
    category = relationship('PostCategory', back_populates='post')
    content = relationship('PostContent', back_populates='post')
    comment = relationship('Comment', back_populates='post')


class PostContent(Base):
    __tablename__ = 'post_content'

    id = Column(Uuid, primary_key=True)
    version = Column(Integer, nullable=False, default=0)
    date_upd = Column(DateTime, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    id_post = Column(Uuid, ForeignKey(Post.id), nullable=False)

    post = relationship('Post', back_populates='content')


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