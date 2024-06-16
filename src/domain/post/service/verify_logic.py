from fastapi import HTTPException
from starlette import status

from src.core.exception import InvalidUserError
from src.dependency import ports
from src.domain.user.model import user_request


async def verify_author(
    *,
    user: user_request.UserCurrent,
    repo: ports.PostRepository,
    post_id: int,
) -> None:
    post = await repo.read_post_by_id(post_id=post_id)
    if post.user_id != user.id:
        raise InvalidUserError


async def verify_comment(
    *,
    repo: ports.CommentRepository,
    post_id: int,
) -> None:
    comment = await repo.read_comment_by_post_id(post_id=post_id)
    if comment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can't delete commented post",
        )
