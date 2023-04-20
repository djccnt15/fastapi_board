from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from sql_app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_superuser = Column(Boolean)
    is_staff = Column(Boolean)
    date_create = Column(DateTime, nullable=False)

    questions: Mapped[list["Question"]] = relationship(back_populates="user")
    answers: Mapped[list["Answer"]] = relationship(back_populates="user")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    date_create = Column(DateTime, nullable=False)

    user: Mapped["User"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    content = Column(Text, nullable=False)
    date_create = Column(DateTime, nullable=False)
    id_question = Column(Integer, ForeignKey("question.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship(back_populates="answers")