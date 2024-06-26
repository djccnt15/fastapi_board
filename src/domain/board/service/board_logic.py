from datetime import datetime
from typing import Iterable, Sequence

from fastapi import HTTPException
from starlette import status

from src import dependency
from src.core.configs import KST
from src.db.entity.post_entity import PostCategoryEntity


async def get_board_list(
    *,
    repo: dependency.CategoryRepo,
) -> Sequence[PostCategoryEntity]:
    category_list = await repo.read_t1_category_list()
    return category_list


async def get_category_list(
    *,
    repo: dependency.CategoryRepo,
    board: str,
) -> Sequence[PostCategoryEntity]:
    category_list = await repo.read_t2_category_list(category=board)
    return category_list


async def get_parent_category(
    *,
    repo: dependency.CategoryRepo,
    category: str,
) -> PostCategoryEntity | None:
    parent_category = await repo.read_parent_category(category=category)
    return parent_category


async def get_category_id(
    *,
    repo: dependency.CategoryRepo,
    category: str,
) -> PostCategoryEntity:
    post_category = await repo.read_category_id(category=category)
    if not post_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no such category",
        )
    return post_category


async def get_post_count(
    *,
    repo: dependency.PostRepo,
    category: int,
    keyword: str | None,
) -> int:
    count = await repo.read_post_count(category_id=category, keyword=keyword)
    if not count:
        return 0
    return int(count)


async def get_post_list(
    *,
    repo: dependency.PostRepo,
    board: int,
    keyword: str | None,
    size: int,
    page: int,
) -> Iterable[dict]:
    post_list = await repo.read_post_list(
        category_id=board,
        keyword=keyword,
        size=size,
        page=page,
    )
    return post_list


async def create_post(
    *,
    repo: dependency.PostRepo,
    category: int,
    user_id: int,
    title: str,
    content: str,
) -> None:
    post_id = await repo.create_post(
        category_id=category,
        created_datetime=datetime.now(KST),
        user_id=user_id,
    )

    await repo.create_post_detail(
        created_datetime=datetime.now(KST),
        title=title,
        content=content,
        post_id=post_id if post_id else 0,
    )
