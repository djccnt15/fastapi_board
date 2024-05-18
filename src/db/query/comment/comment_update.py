from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from src.db.entity.comment_entity import CommentContentEntity


async def update_comment(
    *,
    db: AsyncSession,
    version: int,
    datetime: datetime,
    content: str,
    comment_id: int,
):
    q = insert(CommentContentEntity).values(
        version=version,
        created_datetime=datetime,
        content=content,
        comment_id=comment_id,
    )
    await db.execute(q)
    await db.commit()
