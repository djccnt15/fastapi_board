from datetime import datetime
from typing import Iterable, Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.configs import KST
from src.db.entity import PostCategoryEntity
from src.db.query.board import board_read
from src.db.query.post import post_create, post_read


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


async def get_category_id(
    *,
    db: AsyncSession,
    category: str,
) -> PostCategoryEntity:
    post_category = await board_read.read_category_id(db=db, category=category)
    if not post_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no such category",
        )
    return post_category


async def get_post_count(
    *,
    db: AsyncSession,
    category: int,
    keyword: str,
) -> int:
    count = await post_read.read_post_count(
        db=db,
        category_id=category,
        keyword=keyword,
    )
    if not count:
        return 0
    return int(count)


async def get_post_list(
    *,
    db: AsyncSession,
    board: int,
    keyword: str,
    size: int,
    page: int,
) -> Iterable[dict]:
    post_list = await post_read.read_post_list(
        db=db,
        category_id=board,
        keyword=keyword,
        size=size,
        page=page,
    )
    return post_list


async def create_post(
    *,
    db: AsyncSession,
    category: int,
    user_id: int,
    title: str,
    content: str,
) -> None:
    post_id = await post_create.create_post(
        db=db,
        category_id=category,
        created_datetime=datetime.now(KST),
        user_id=user_id,
    )

    await post_create.create_post_detail(
        db=db,
        created_datetime=datetime.now(KST),
        title=title,
        content=content,
        post_id=post_id if post_id else 0,
    )
