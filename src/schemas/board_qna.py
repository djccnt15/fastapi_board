from datetime import datetime

from pydantic import BaseModel

from src.schemas.user import User


class Answer(BaseModel):
    id: int
    content: str
    user: User
    date_create: datetime

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: int
    subject: str
    content: str
    user: User
    date_create: datetime
    answers: list[Answer] = []

    class Config:
        orm_mode = True