from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.entity.post_entity import PostContentEntity


async def update_post(
    *,
    db: AsyncSession,
    version: int,
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
