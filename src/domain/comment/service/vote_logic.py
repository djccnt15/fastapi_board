from sqlalchemy.ext.asyncio import AsyncSession

from src.db.query.comment import comment_create, comment_delete
from src.domain.user.model import user_request


async def vote_comment(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    comment_id: int,
) -> None:
    await comment_create.create_comment_vote(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
    )


async def revoke_vote_post(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    comment_id: int,
) -> None:
    await comment_delete.delete_comment_vote(
        db=db,
        user_id=current_user.id,
        comment_id=comment_id,
    )
