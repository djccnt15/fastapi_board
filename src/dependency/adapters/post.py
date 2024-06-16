from datetime import datetime
from typing import Iterable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, func, insert, select, text, update

from src.core.configs import RESOURCES
from src.db.entity.post_entity import (
    PostCategoryEntity,
    PostContentEntity,
    PostEntity,
    PostVoterEntity,
)
from src.db.entity.user_entity import UserEntity
from src.dependency.ports import PostRepository

SQL_PATH = RESOURCES / "sql"

with open(file=SQL_PATH / "post_count.sql", encoding="utf-8") as f:
    POST_COUNT_QUERY = f.read()

with open(file=SQL_PATH / "post_list.sql", encoding="utf-8") as f:
    POST_LIST_QUERY = f.read()

with open(file=SQL_PATH / "post_list_keyword_where.sql", encoding="utf-8") as f:
    POST_LIST_QUERY_KEYWORD_WHERE = f.read()

with open(file=SQL_PATH / "post_list_order_limit.sql", encoding="utf-8") as f:
    POST_LIST_QUERY_ORDER_LIMIT = f.read()


class RdbPostRepository(PostRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def create_post(
        self,
        *,
        category_id: int,
        created_datetime: datetime,
        user_id: int,
    ) -> int:
        q = (
            insert(PostEntity)
            .values(
                user_id=user_id,
                category_id=category_id,
                created_datetime=created_datetime,
            )
            .returning(PostEntity.id)
        )
        res = await self.db.execute(statement=q)
        created_id = res.scalar_one()
        await self.db.commit()
        return created_id

    async def create_post_detail(
        self,
        *,
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
        await self.db.execute(statement=q)
        await self.db.commit()

    async def read_post_count(
        self,
        *,
        category_id: int,
        keyword: str | None = None,
    ) -> int:
        q = POST_COUNT_QUERY

        if keyword:
            keyword = f"%{keyword}%"
            q += POST_LIST_QUERY_KEYWORD_WHERE

        param = {
            "category_id": category_id,
            "keyword": keyword,
        }
        res = await self.db.execute(statement=text(q), params=param)
        return res.scalar_one()

    async def read_post_list(
        self,
        *,
        category_id: int,
        keyword: str | None,
        size: int,
        page: int,
    ) -> Iterable[dict]:
        q = POST_LIST_QUERY

        if keyword:
            keyword = f"%{keyword}%"
            q += POST_LIST_QUERY_KEYWORD_WHERE

        q += POST_LIST_QUERY_ORDER_LIMIT

        param = {
            "category_id": category_id,
            "keyword": keyword,
            "size": size,
            "page": page,
        }
        res = await self.db.execute(statement=text(q), params=param)
        result_dicts = (dict(zip(res.keys(), row)) for row in res.all())
        return result_dicts

    async def read_post(self, *, post_id: int) -> dict:
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
        res = await self.db.execute(statement=q)
        row = res.one()
        result_dicts = dict(zip(res.keys(), row))
        return result_dicts

    async def read_post_by_id(self, *, post_id: int) -> PostEntity:
        q = select(PostEntity).where(PostEntity.id == post_id)
        res = await self.db.execute(statement=q)
        return res.scalar_one()

    async def read_post_last_version(self, *, post_id: int) -> int:
        q = (
            select(func.max(PostContentEntity.version))
            .where(PostContentEntity.post_id == post_id)
            .group_by(PostContentEntity.post_id)
        )
        res = await self.db.execute(statement=q)
        return res.scalar_one()

    async def read_post_history(self, *, post_id: int) -> Sequence[PostContentEntity]:
        q = (
            select(PostContentEntity)
            .where(PostContentEntity.post_id == post_id)
            .order_by(PostContentEntity.id)
        )
        res = await self.db.execute(q)
        return res.scalars().all()

    async def inactivate_post(self, *, post_id: int) -> None:
        q = update(PostEntity).where(PostEntity.id == post_id).values(is_active=False)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def create_post_vote(
        self,
        *,
        post_id: int,
        user_id: int,
    ) -> None:
        q = insert(PostVoterEntity).values(user_id=user_id, post_id=post_id)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def delete_post_vote(
        self,
        *,
        user_id: int,
        post_id: int,
    ) -> None:
        q = delete(PostVoterEntity).where(
            PostVoterEntity.user_id == user_id,
            PostVoterEntity.post_id == post_id,
        )
        await self.db.execute(statement=q)
        await self.db.commit()
