from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, update

from src.db.entity.comment_entity import CommentEntity, CommentVoterEntity


async def delete_comment(
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


async def delete_comment_vote(
    *,
    db: AsyncSession,
    user_id: int,
    comment_id: int,
):
    q = delete(CommentVoterEntity).where(
        CommentVoterEntity.user_id == user_id,
        CommentVoterEntity.comment_id == comment_id,
    )
    await db.execute(q)
    await db.commit()
