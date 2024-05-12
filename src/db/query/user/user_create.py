from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.common.configs import KST
from src.db.entity.user_entity import LoggedInEntity, UserEntity


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
    await db.execute(statement=q)
    await db.commit()


async def create_login_his(
    *,
    db: AsyncSession,
    user_id: int,
) -> None:
    q = insert(LoggedInEntity).values(
        user_id=user_id,
        created_datetime=datetime.now(KST),
    )
    await db.execute(statement=q)
    await db.commit()
