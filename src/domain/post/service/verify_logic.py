from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.exception import InvalidUserError, QueryResultEmptyError
from src.db.query.comment import comment_read
from src.db.query.post import post_read
from src.domain.user.model import user_request


async def verify_author(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
) -> None:
    post = await post_read.read_post_by_id(db=db, post_id=post_id)
    if not post:
        raise QueryResultEmptyError
    elif post.user_id != current_user.id:
        raise InvalidUserError


async def verify_comment(
    *,
    db: AsyncSession,
    post_id: int,
) -> None:
    comment = await comment_read.read_comment_by_post_id(db=db, post_id=post_id)
    if comment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can't delete commented post",
        )
