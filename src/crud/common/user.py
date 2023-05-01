from datetime import datetime

from sqlalchemy.orm import Session
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
    q = db \
        .query(User) \
        .filter(User.email == user_create.email) \
        .first()
    return q


def get_existing_username(db: Session, user_create: UserCreate):
    q = db \
        .query(User) \
        .filter(User.username == user_create.username) \
        .first()
    return q