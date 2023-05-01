from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from settings.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    is_superuser = Column(Boolean, default=None)
    is_staff = Column(Boolean, default=None)
    date_create = Column(DateTime, nullable=False)
    is_blocked = Column(Boolean, default=None)
    is_active = Column(Boolean, nullable=False, default=True)

    post: Mapped[list['Post']] = relationship(back_populates='user')
    comment: Mapped[list['Comment']] = relationship(back_populates='user')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    tier = Column(Integer, nullable=False)
    category = Column(String(length=255), nullable=False)
    id_parent = Column(Integer, ForeignKey('category.id'))

    child = relationship(argument='Category', remote_side=[id])
    post: Mapped[list['Post']] = relationship(back_populates='category')


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    id_category = Column(Integer, ForeignKey(Category.id), nullable=False)
    date_create = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    user: Mapped['User'] = relationship(back_populates='post')
    category: Mapped[list['Category']] = relationship(back_populates='post')
    content: Mapped[list['PostContent']] = relationship(back_populates='post')
    comment: Mapped[list['Comment']] = relationship(back_populates='post')


class PostContent(Base):
    __tablename__ = 'post_content'

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    date_upd = Column(DateTime, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    id_post = Column(Integer, ForeignKey(Post.id), nullable=False)

    post: Mapped['Post'] = relationship(back_populates='content')


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    id_post = Column(Integer, ForeignKey(Post.id), nullable=False)
    date_create = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    user: Mapped['User'] = relationship(back_populates='comment')
    post: Mapped['Post'] = relationship(back_populates='comment')
    content: Mapped[list['CommentContent']] = relationship(back_populates='comment')


class CommentContent(Base):
    __tablename__ = 'comment_content'

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    date_upd = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    id_comment = Column(Integer, ForeignKey(Comment.id), nullable=False)

    comment: Mapped['Comment'] = relationship(back_populates='content')