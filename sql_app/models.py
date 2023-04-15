from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_superuser = Column(Boolean)
    is_staff = Column(Boolean)


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", backref="questions")
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", backref="answers")
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    id_question = Column(Integer, ForeignKey("question.id"), nullable=False)
    question = relationship("Question", backref="answers")