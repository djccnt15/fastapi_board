from uuid import uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.sql import insert, select, update

from conf.security import pwd_context
from src.models import *
from src.schemas import UserCreate


async def create_user(db: AsyncSession, user_create: UserCreate):
    q = insert(User) \
        .values(
            username=user_create.username,
            password=pwd_context.hash(user_create.password1),
            date_create=datetime.now(),
            email=user_create.email
        )
    await db.execute(q)
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


async def get_conflict_user(db: AsyncSession, user_create: UserCreate, id: int):
    q = select(User) \
        .where(
            (User.id != id) &
            ((User.email == user_create.email) |
            (User.username == user_create.username))
        )
    res = await db.execute(q)
    return res.scalars().all()


async def update_user(db: AsyncSession, user_update: UserCreate, id: int):
    q = update(User) \
        .where(User.id == id) \
        .values({
            User.username: user_update.username,
            User.email: user_update.email,
            User.password: pwd_context.hash(user_update.password1)
        })
    await db.execute(q)
    await db.commit()


async def del_user(db: AsyncSession, id: int):
    q = update(User) \
        .where(User.id == id) \
        .values(username=None, email=None)
    await db.execute(q)
    await db.commit()


async def get_manage(db: AsyncSession, name: str):
    q = select(Manage) \
        .where(Manage.name == name)
    res = await db.execute(q)
    return res.scalar()


async def create_user_manage(
        db: AsyncSession,
        id_user: int,
        id_manage: int,
        detail: str | None = None
):
    q = insert(UserManage) \
        .values(
            id=uuid4(),
            id_user=id_user,
            id_manage=id_manage,
            detail=detail,
            date_create=datetime.now()
        )
    await db.execute(q)
    await db.commit()


async def get_user_manage(db: AsyncSession, id: str):
    q = select(Manage) \
        .join(UserManage) \
        .where(UserManage.id_user == id)
    res = await db.execute(q)
    return res.scalar()


async def create_log(engine: AsyncEngine, date_create: datetime, log: str):
    async with engine.connect() as conn:
        q = insert(Log).values(id=uuid4(), date_create=date_create, log=log)
        await conn.execute(q)
        await conn.commit()


async def create_login_his(db: AsyncSession, id_user: int):
    q = insert(LoggedIn) \
        .values(
            id=uuid4(),
            id_user=id_user,
            date_create=datetime.now()
        )
    await db.execute(q)
    await db.commit()