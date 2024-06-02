from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.entity.user_entity import LoggedInEntity, UserEntity


async def create_user(
    *,
    db: AsyncSession,
    name: str,
    password: str,
    email: str,
    created_datetime: datetime,
) -> None:
    q = insert(UserEntity).values(
        name=name,
        password=password,
        email=email,
        created_datetime=created_datetime,
    )
    await db.execute(statement=q)
    await db.commit()


async def create_login_log(
    *,
    db: AsyncSession,
    user_id: int,
    created_datetime: datetime,
) -> None:
    q = insert(LoggedInEntity).values(
        user_id=user_id,
        created_datetime=created_datetime,
    )
    await db.execute(statement=q)
    await db.commit()
