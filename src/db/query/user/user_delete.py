from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from src.db.entity.user_entity import UserEntity


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
    await db.execute(statement=q)
    await db.commit()
