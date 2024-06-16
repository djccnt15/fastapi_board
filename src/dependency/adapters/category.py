from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import select

from src.db.entity.post_entity import PostCategoryEntity
from src.dependency.ports import CategoryRepository


class RdbCategoryRepository(CategoryRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def read_t1_category_list(self) -> Sequence[PostCategoryEntity]:
        q = select(PostCategoryEntity).where(PostCategoryEntity.tier == 1)
        res = await self.db.execute(q)
        return res.scalars().all()

    async def read_t2_category_list(
        self, *, category: str
    ) -> Sequence[PostCategoryEntity]:
        tier_1 = aliased(PostCategoryEntity)
        q = (
            select(PostCategoryEntity)
            .join(PostCategoryEntity.parent.of_type(tier_1))
            .where(tier_1.name == category)
        )
        res = await self.db.execute(q)
        return res.scalars().all()

    async def read_parent_category(self, *, category: str) -> PostCategoryEntity:
        parent = aliased(PostCategoryEntity)
        q = (
            select(parent)
            .join(PostCategoryEntity.parent.of_type(parent))
            .where(PostCategoryEntity.name == category)
        )
        res = await self.db.execute(q)
        return res.scalar_one()

    async def read_category_id(self, *, category: str) -> PostCategoryEntity:
        q = select(PostCategoryEntity).where(PostCategoryEntity.name == category)
        res = await self.db.execute(statement=q)
        return res.scalar_one()
