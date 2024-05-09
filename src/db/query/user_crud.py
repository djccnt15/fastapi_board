from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, or_, select, update

from src.common.configs import KST
from src.db.entity.user_entity import (
    LoggedInEntity,
    StateEntity,
    UserEntity,
    UserStateEntity,
)


async def create_user(
    *,
    db: AsyncSession,
    name: str,
    password: str,
    email: str,
) -> None:
    q = insert(UserEntity).values(
        name=name,
        password=password,
        email=email,
        created_datetime=datetime.now(KST),
    )
    await db.execute(q)
    await db.commit()


async def read_user_by_name_email(
    *,
    db: AsyncSession,
    name: str,
    email: str,
) -> Sequence[UserEntity]:
    q = select(UserEntity).where(
        or_(
            UserEntity.name == name,
            UserEntity.email == email,
        )
    )
    res = await db.execute(q)
    return res.scalars().all()


async def read_user_by_name(
    *,
    db: AsyncSession,
    name: str,
) -> UserEntity | None:
    q = select(UserEntity).where(UserEntity.name == name)
    res = await db.execute(q)
    return res.scalar()


async def update_user(
    *,
    db: AsyncSession,
    user_id: int,
    name: str,
    email: str,
) -> None:
    q = (
        update(UserEntity)
        .where(UserEntity.id == user_id)
        .values(name=name, email=email)
    )
    await db.execute(q)
    await db.commit()


async def update_password(
    *,
    db: AsyncSession,
    user_id: int,
    password: str,
) -> None:
    q = update(UserEntity).where(UserEntity.id == user_id).values(password=password)
    await db.execute(q)
    await db.commit()


async def delete_user(
    *,
    db: AsyncSession,
    user_id: int,
) -> None:
    q = (
        update(UserEntity)
        .where(UserEntity.id == user_id)
        .values(name=None, password=None, email=None)
    )
    await db.execute(q)
    await db.commit()


async def read_user_state(
    *,
    db: AsyncSession,
    user_id: str,
) -> StateEntity | None:
    q = (
        select(StateEntity)
        .join(UserStateEntity)
        .where(UserStateEntity.user_id == user_id)
    )
    res = await db.execute(q)
    return res.scalar()


async def create_login_his(
    *,
    db: AsyncSession,
    user_id: int,
) -> None:
    q = insert(LoggedInEntity).values(
        user_id=user_id,
        created_datetime=datetime.now(KST),
    )
    await db.execute(q)
    await db.commit()
