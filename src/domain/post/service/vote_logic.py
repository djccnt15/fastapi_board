from src.dependency import ports
from src.domain.user.model import user_request


async def vote_post(
    *,
    user: user_request.UserCurrent,
    repo: ports.PostRepository,
    post_id: int,
) -> None:
    await repo.create_post_vote(post_id=post_id, user_id=user.id)


async def revoke_vote_post(
    *,
    user: user_request.UserCurrent,
    repo: ports.PostRepository,
    post_id: int,
) -> None:
    await repo.delete_post_vote(user_id=user.id, post_id=post_id)
