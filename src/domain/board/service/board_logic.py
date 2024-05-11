from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.entity import PostCategoryEntity
from src.db.query.board import board_read


async def get_board_list(*, db: AsyncSession) -> Sequence[PostCategoryEntity]:
    category_list = await board_read.read_t1_category_list(db=db)
    return category_list


async def get_category_list(
    *,
    db: AsyncSession,
    board: str,
) -> Sequence[PostCategoryEntity]:
    category_list = await board_read.read_t2_category_list(db=db, parent=board)
    return category_list


async def get_parent_category(
    *,
    db: AsyncSession,
    category: str,
) -> PostCategoryEntity | None:
    parent_category = await board_read.read_parent_category(db=db, category=category)
    return parent_category
