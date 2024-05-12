from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from src.db.entity.user_entity import UserEntity


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
    await db.execute(statement=q)
    await db.commit()


async def update_password(
    *,
    db: AsyncSession,
    user_id: int,
    password: str,
) -> None:
    q = update(UserEntity).where(UserEntity.id == user_id).values(password=password)
    await db.execute(statement=q)
    await db.commit()
