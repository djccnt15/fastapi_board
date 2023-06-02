from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from passlib.context import CryptContext

from src.models.models import User
from src.schemas.common.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        date_create=datetime.now(),
        email=user_create.email
    )
    db.add(db_user)
    db.commit()


def get_existing_useremail(db: Session, user_create: UserCreate):
    q = select(User).where(User.email == user_create.email)
    return db.execute(q).scalar()


def get_existing_username(db: Session, user_create: UserCreate):
    q = select(User).where(User.username == user_create.username)
    return db.execute(q).scalar()