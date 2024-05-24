from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete

from src.db.entity.post_entity import PostVoterEntity


async def delete_post_vote(
    *,
    db: AsyncSession,
    user_id: int,
    post_id: int,
) -> None:
    q = delete(PostVoterEntity).where(
        PostVoterEntity.user_id == user_id,
        PostVoterEntity.post_id == post_id,
    )
    await db.execute(statement=q)
    await db.commit()
