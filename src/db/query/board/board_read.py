from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import select

from src.db.entity.post_entity import PostCategoryEntity


async def read_t1_category_list(db: AsyncSession) -> Sequence[PostCategoryEntity]:
    q = select(PostCategoryEntity).where(PostCategoryEntity.tier == 1)
    res = await db.execute(q)
    return res.scalars().all()


async def read_t2_category_list(
    *,
    db: AsyncSession,
    parent: str,
) -> Sequence[PostCategoryEntity]:
    tier_1 = aliased(PostCategoryEntity)
    q = (
        select(PostCategoryEntity)
        .join(PostCategoryEntity.parent.of_type(tier_1))
        .where(tier_1.name == parent)
    )
    res = await db.execute(q)
    return res.scalars().all()


async def read_parent_category(
    *,
    db: AsyncSession,
    category: str,
) -> PostCategoryEntity | None:
    parent = aliased(PostCategoryEntity)
    q = (
        select(parent)
        .join(PostCategoryEntity.parent.of_type(parent))
        .where(PostCategoryEntity.name == category)
    )
    res = await db.execute(q)
    return res.scalar()


async def read_category_id(
    *,
    db: AsyncSession,
    category: str,
) -> PostCategoryEntity | None:
    q = select(PostCategoryEntity).where(PostCategoryEntity.name == category)
    res = await db.execute(statement=q)
    return res.scalar()
