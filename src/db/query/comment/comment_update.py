from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import update

from src.db.entity.comment_entity import CommentEntity


async def inactivate_comment(
    *,
    db: AsyncSession,
    comment_id: int,
):
    q = (
        update(CommentEntity)
        .where(CommentEntity.id == comment_id)
        .values(is_active=False)
    )
    await db.execute(q)
    await db.commit()
