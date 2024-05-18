from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.configs import KST
from src.db.entity.comment_entity import CommentContentEntity
from src.db.query.comment import comment_delete, comment_read, comment_update
from src.domain.comment.model import comment_request


async def get_comment_history(
    *,
    db: AsyncSession,
    comment_id: int,
) -> Sequence[CommentContentEntity]:
    comment_list = await comment_read.read_comment_history(db=db, comment_id=comment_id)
    return comment_list


async def update_comment(
    *,
    db: AsyncSession,
    data: comment_request.CommentBaseRequest,
    comment_id: int,
) -> None:
    version = await comment_read.read_comment_last_version(db=db, comment_id=comment_id)
    if not version:
        version = 0

    await comment_update.update_comment(
        db=db,
        version=version + 1,
        datetime=datetime.now(KST),
        content=data.content,
        comment_id=comment_id,
    )


async def delete_comment(
    *,
    db: AsyncSession,
    comment_id: int,
):
    await comment_delete.delete_comment(db=db, comment_id=comment_id)
