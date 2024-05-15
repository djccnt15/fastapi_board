from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, update

from src.db.entity.post_entity import PostEntity, PostVoterEntity


async def delete_post(
    *,
    db: AsyncSession,
    post_id: int,
) -> None:
    q = update(PostEntity).where(PostEntity.id == post_id).values(is_active=False)
    await db.execute(statement=q)
    await db.commit()


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
