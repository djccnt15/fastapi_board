from src.dependency import ports
from src.domain.user.model import user_request


async def vote_comment(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    comment_id: int,
) -> None:
    await repo.create_comment_vote(comment_id=comment_id, user_id=user.id)


async def revoke_vote_post(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    comment_id: int,
) -> None:
    await repo.delete_comment_vote(user_id=user.id, comment_id=comment_id)
