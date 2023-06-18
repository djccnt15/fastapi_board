from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from passlib.context import CryptContext

from src.models import User
from src.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(db: AsyncSession, user_create: UserCreate):
    db_user = User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        date_create=datetime.now(),
        email=user_create.email
    )
    db.add(db_user)
    await db.commit()


async def get_existing_user(db: AsyncSession, user_create: UserCreate):
    q = select(User) \
        .where(
        (User.email == user_create.email) |
        (User.username == user_create.username)
        )
    res = await db.execute(q)
    return res.scalars().all()


async def get_user(db: AsyncSession, username: str):
    q = select(User) \
        .where(User.username == username)
    res = await db.execute(q)
    return res.scalar()