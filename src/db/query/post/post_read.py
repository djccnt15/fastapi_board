from typing import Any, Iterable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select, text

from src.core.exception import QueryResultEmptyError
from src.db.entity.post_entity import PostCategoryEntity, PostContentEntity, PostEntity
from src.db.entity.user_entity import UserEntity
from src.db.query import sql


async def read_post_count(
    *,
    db: AsyncSession,
    category_id: int,
    keyword: str | None = None,
) -> Any | None:
    q = sql.POST_COUNT_QUERY

    if keyword:
        keyword = f"%{keyword}%"
        q += sql.POST_LIST_QUERY_KEYWORD_WHERE

    param = {
        "category_id": category_id,
        "keyword": keyword,
    }
    res = await db.execute(statement=text(q), params=param)
    return res.scalar()


async def read_post_list(
    *,
    db: AsyncSession,
    category_id: int,
    keyword: str,
    size: int,
    page: int,
) -> Iterable[dict[Any, Any]]:
    q = sql.POST_LIST_QUERY

    if keyword:
        keyword = f"%{keyword}%"
        q += sql.POST_LIST_QUERY_KEYWORD_WHERE

    q += sql.POST_LIST_QUERY_ORDER_LIMIT

    param = {
        "category_id": category_id,
        "keyword": keyword,
        "size": size,
        "page": page,
    }
    res = await db.execute(statement=text(q), params=param)
    result_dicts = (dict(zip(res.keys(), row)) for row in res.all())
    return result_dicts


async def read_post(
    *,
    db: AsyncSession,
    post_id: int,
) -> dict:
    version_subq = (
        select(
            PostContentEntity.post_id.label("post_id"),
            func.max(PostContentEntity.version).label("last"),
        )
        .group_by(PostContentEntity.post_id)
        .subquery()
    )

    content_subq = (
        select(PostContentEntity)
        .join(
            target=version_subq,
            onclause=(
                (PostContentEntity.post_id == version_subq.c.post_id)
                & (PostContentEntity.version == version_subq.c.last)
            ),
        )
        .subquery()
    )

    q = (
        select(
            PostEntity,
            UserEntity,
            PostCategoryEntity,
            content_subq,
        )
        .join(
            target=UserEntity,
            onclause=PostEntity.user_id == UserEntity.id,
        )
        .join(
            target=PostCategoryEntity,
            onclause=PostEntity.category_id == PostCategoryEntity.id,
        )
        .join(
            target=content_subq,
            onclause=PostEntity.id == content_subq.c.post_id,
        )
        .where(
            PostEntity.is_active,
            PostEntity.id == post_id,
        )
    )
    res = await db.execute(statement=q)
    row = res.first()
    if not row:
        raise QueryResultEmptyError
    result_dicts = dict(zip(res.keys(), row))
    return result_dicts


async def read_post_by_id(
    *,
    db: AsyncSession,
    post_id: int,
) -> PostEntity | None:
    q = select(PostEntity).where(PostEntity.id == post_id)
    res = await db.execute(statement=q)
    return res.scalar()


async def read_post_last_version(
    *,
    db: AsyncSession,
    post_id: int,
) -> int | None:
    q = (
        select(func.max(PostContentEntity.version))
        .where(PostContentEntity.post_id == post_id)
        .group_by(PostContentEntity.post_id)
    )
    res = await db.execute(statement=q)
    return res.scalar()


async def read_post_history(
    *,
    db: AsyncSession,
    post_id: int,
) -> Sequence[PostContentEntity]:
    q = select(PostContentEntity).where(PostContentEntity.post_id == post_id)
    res = await db.execute(q)
    return res.scalars().all()
