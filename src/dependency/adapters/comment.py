from datetime import datetime
from typing import Iterable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, func, insert, select, text, update

from src.core.configs import RESOURCES
from src.db.entity.comment_entity import (
    CommentContentEntity,
    CommentEntity,
    CommentVoterEntity,
)
from src.dependency.ports import CommentRepository

SQL_PATH = RESOURCES / "sql"

with open(file=SQL_PATH / "comment_list.sql", encoding="utf-8") as f:
    COMMENT_LIST_QUERY = f.read()


class RdbCommentRepository(CommentRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def create_comment(
        self,
        *,
        user_id: int,
        post_id: int,
        created_datetime: datetime,
    ) -> int:
        q = (
            insert(CommentEntity)
            .values(
                user_id=user_id,
                post_id=post_id,
                created_datetime=created_datetime,
            )
            .returning(CommentEntity.id)
        )
        res = await self.db.execute(q)
        created_id = res.scalar_one()
        await self.db.commit()
        return created_id

    async def create_comment_detail(
        self,
        *,
        version: int | None = None,
        created_datetime: datetime,
        content: str,
        comment_id: int,
    ) -> None:
        q = insert(CommentContentEntity).values(
            version=version,
            created_datetime=created_datetime,
            content=content,
            comment_id=comment_id,
        )
        await self.db.execute(q)
        await self.db.commit()

    async def read_comment_by_id(self, *, comment_id: int) -> CommentEntity:
        q = (
            select(CommentEntity)
            .where(CommentEntity.id == comment_id)
            .order_by(CommentEntity.id)
        )
        res = await self.db.execute(statement=q)
        return res.scalar_one()

    async def read_comment_by_post_id(self, *, post_id: int) -> Sequence[CommentEntity]:
        q = (
            select(CommentEntity)
            .where(CommentEntity.post_id == post_id)
            .order_by(CommentEntity.id)
        )
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_comment_list(self, *, post_id: int) -> Iterable[dict]:
        q = COMMENT_LIST_QUERY
        param = {"post_id": post_id}

        res = await self.db.execute(statement=text(q), params=param)
        result_dicts = (dict(zip(res.keys(), row)) for row in res.all())
        return result_dicts

    async def read_comment_last_version(self, *, comment_id: int) -> int:
        q = (
            select(func.max(CommentContentEntity.version))
            .where(CommentContentEntity.comment_id == comment_id)
            .group_by(CommentContentEntity.comment_id)
        )
        res = await self.db.execute(statement=q)
        return res.scalar_one()

    async def read_comment_history(
        self, *, comment_id: int
    ) -> Sequence[CommentContentEntity]:
        q = (
            select(CommentContentEntity)
            .where(CommentContentEntity.comment_id == comment_id)
            .order_by(CommentContentEntity.id)
        )
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def inactivate_comment(self, *, comment_id: int) -> None:
        q = (
            update(CommentEntity)
            .where(CommentEntity.id == comment_id)
            .values(is_active=False)
        )
        await self.db.execute(q)
        await self.db.commit()

    async def create_comment_vote(
        self,
        *,
        comment_id: int,
        user_id: int,
    ) -> None:
        q = insert(CommentVoterEntity).values(user_id=user_id, comment_id=comment_id)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def delete_comment_vote(
        self,
        *,
        user_id: int,
        comment_id: int,
    ) -> None:
        q = delete(CommentVoterEntity).where(
            CommentVoterEntity.user_id == user_id,
            CommentVoterEntity.comment_id == comment_id,
        )
        await self.db.execute(q)
        await self.db.commit()
