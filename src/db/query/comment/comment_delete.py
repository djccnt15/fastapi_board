from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete

from src.db.entity.comment_entity import CommentVoterEntity


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
