from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import or_, select

from src.db.entity.user_entity import UserEntity


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
    res = await db.execute(statement=q)
    return res.scalars().all()


async def read_user_by_name(
    *,
    db: AsyncSession,
    name: str,
) -> UserEntity | None:
    q = select(UserEntity).where(UserEntity.name == name)
    res = await db.execute(statement=q)
    return res.scalar()
