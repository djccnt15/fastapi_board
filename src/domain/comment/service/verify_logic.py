from src.core.exception import InvalidUserError
from src.dependency import ports
from src.domain.user.model import user_request


async def verify_author(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    comment_id: int,
) -> None:
    comment = await repo.read_comment_by_id(comment_id=comment_id)
    if comment.user_id != user.id:
        raise InvalidUserError
