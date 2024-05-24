from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.entity.post_entity import PostContentEntity, PostEntity, PostVoterEntity


async def create_post(
    *,
    db: AsyncSession,
    category_id: int,
    created_datetime: datetime,
    user_id: int,
) -> Any | None:
    q = (
        insert(PostEntity)
        .values(
            user_id=user_id,
            category_id=category_id,
            created_datetime=created_datetime,
        )
        .returning(PostEntity.id)
    )
    res = await db.execute(statement=q)
    created_id = res.scalar()
    await db.commit()
    return created_id


async def create_post_detail(
    *,
    db: AsyncSession,
    version: int | None = None,
    created_datetime: datetime,
    title: str,
    content: str,
    post_id: int,
) -> None:
    q = insert(PostContentEntity).values(
        version=version,
        created_datetime=created_datetime,
        title=title,
        content=content,
        post_id=post_id,
    )
    await db.execute(statement=q)
    await db.commit()


async def create_post_vote(
    *,
    db: AsyncSession,
    post_id: int,
    user_id: int,
) -> None:
    q = insert(PostVoterEntity).values(user_id=user_id, post_id=post_id)
    await db.execute(statement=q)
    await db.commit()
