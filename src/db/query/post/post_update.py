from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from src.db.entity.post_entity import PostEntity


async def inactivate_post(
    *,
    db: AsyncSession,
    post_id: int,
) -> None:
    q = update(PostEntity).where(PostEntity.id == post_id).values(is_active=False)
    await db.execute(statement=q)
    await db.commit()
