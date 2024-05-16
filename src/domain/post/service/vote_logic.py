from sqlalchemy.ext.asyncio import AsyncSession

from src.db.query.post import post_create, post_delete
from src.domain.user.model import user_request


async def vote_post(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
) -> None:
    await post_create.create_post_vote(db=db, post_id=post_id, user_id=current_user.id)


async def revoke_vote_post(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
) -> None:
    await post_delete.delete_post_vote(db=db, user_id=current_user.id, post_id=post_id)
