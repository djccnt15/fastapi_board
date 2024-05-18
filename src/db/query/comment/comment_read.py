from typing import Iterable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select, text

from src.db.entity.comment_entity import CommentContentEntity, CommentEntity
from src.db.query import sql


async def read_comment_by_id(
    *,
    db: AsyncSession,
    comment_id: int,
) -> CommentEntity | None:
    q = select(CommentEntity).where(CommentEntity.id == comment_id)
    res = await db.execute(statement=q)
    return res.scalar()


async def read_comment_list(
    *,
    db: AsyncSession,
    post_id: int,
) -> Iterable[dict]:
    q = sql.COMMENT_LIST_QUERY
    param = {"post_id": post_id}

    res = await db.execute(statement=text(q), params=param)
    result_dicts = (dict(zip(res.keys(), row)) for row in res.all())
    return result_dicts


async def read_comment_last_version(
    *,
    db: AsyncSession,
    comment_id: int,
) -> int | None:

    q = (
        select(func.max(CommentContentEntity.version))
        .where(CommentContentEntity.comment_id == comment_id)
        .group_by(CommentContentEntity.comment_id)
    )
    res = await db.execute(statement=q)
    return res.scalar()


async def read_comment_history(
    *,
    db: AsyncSession,
    comment_id: int,
) -> Sequence[CommentContentEntity]:
    q = select(CommentContentEntity).where(
        CommentContentEntity.comment_id == comment_id
    )
    res = await db.execute(statement=q)
    return res.scalars().all()
