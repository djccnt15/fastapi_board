from datetime import datetime
from typing import Sequence

from src.core.configs import KST
from src.db.entity.comment_entity import CommentContentEntity
from src.dependency import ports
from src.domain.comment.model import comment_request


async def get_comment_history(
    *,
    repo: ports.CommentRepository,
    comment_id: int,
) -> Sequence[CommentContentEntity]:
    comment_list = await repo.read_comment_history(comment_id=comment_id)
    return comment_list


async def update_comment(
    *,
    repo: ports.CommentRepository,
    data: comment_request.CommentCreateRequest,
    comment_id: int,
) -> None:
    version = await repo.read_comment_last_version(comment_id=comment_id)
    await repo.create_comment_detail(
        version=version + 1,
        created_datetime=datetime.now(KST),
        content=data.content,
        comment_id=comment_id,
    )


async def delete_comment(
    *,
    repo: ports.CommentRepository,
    comment_id: int,
) -> None:
    await repo.inactivate_comment(comment_id=comment_id)
