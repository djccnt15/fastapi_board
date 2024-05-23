from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exception import InvalidUserError, QueryResultEmptyError
from src.db.query.comment import comment_read
from src.domain.user.model import user_request


async def verify_author(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    comment_id: int,
) -> None:
    comment = await comment_read.read_comment_by_id(db=db, comment_id=comment_id)
    if not comment:
        raise QueryResultEmptyError
    elif comment.user.id != current_user.id:
        raise InvalidUserError
