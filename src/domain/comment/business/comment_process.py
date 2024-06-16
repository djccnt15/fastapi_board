from typing import Iterable

from sqlalchemy.exc import IntegrityError

from src.dependency import ports
from src.domain.user.model import user_request

from ..model import comment_request, comment_response
from ..service import comment_logic, verify_logic, vote_logic


async def update_comment(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    comment_id: int,
    data: comment_request.CommentCreateRequest,
) -> None:
    await verify_logic.verify_author(repo=repo, user=user, comment_id=comment_id)
    await comment_logic.update_comment(repo=repo, data=data, comment_id=comment_id)


async def delete_comment(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    comment_id: int,
) -> None:
    await verify_logic.verify_author(repo=repo, user=user, comment_id=comment_id)
    await comment_logic.delete_comment(repo=repo, comment_id=comment_id)


async def get_comment_history(
    *,
    repo: ports.CommentRepository,
    comment_id: int,
) -> Iterable[comment_response.CommentContentResponse]:
    history = await comment_logic.get_comment_history(repo=repo, comment_id=comment_id)
    res = (comment_response.CommentContentResponse.model_validate(v) for v in history)
    return res


async def vote_comment(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    comment_id: int,
) -> None:
    try:
        # vote post
        await vote_logic.vote_comment(repo=repo, user=user, comment_id=comment_id)
    except IntegrityError:
        # revoke vote post
        await vote_logic.revoke_vote_post(repo=repo, user=user, comment_id=comment_id)
