from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.entity.comment_entity import (
    CommentContentEntity,
    CommentEntity,
    CommentVoterEntity,
)


async def create_comment(
    *,
    db: AsyncSession,
    user_id: int,
    post_id: int,
    created_datetime: datetime,
) -> Any | None:
    q = (
        insert(CommentEntity)
        .values(
            user_id=user_id,
            post_id=post_id,
            created_datetime=created_datetime,
        )
        .returning(CommentEntity.id)
    )
    res = await db.execute(q)
    created_id = res.scalar()
    await db.commit()
    return created_id


async def create_comment_detail(
    *,
    db: AsyncSession,
    created_datetime: datetime,
    content: str,
    comment_id: int,
):
    q = insert(CommentContentEntity).values(
        created_datetime=created_datetime,
        content=content,
        comment_id=comment_id,
    )
    await db.execute(q)
    await db.commit()


async def create_comment_vote(
    *,
    db: AsyncSession,
    comment_id: int,
    user_id: int,
) -> None:
    q = insert(CommentVoterEntity).values(user_id=user_id, comment_id=comment_id)
    await db.execute(statement=q)
    await db.commit()
