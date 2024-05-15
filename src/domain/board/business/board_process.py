from typing import Iterable

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.domain.post.model import post_request, post_response
from src.domain.user.model import user_request

from ..model import board_response
from ..model.enums import board_enum
from ..service import board_logic


async def get_board_list(db: AsyncSession) -> Iterable[str]:
    category_list = await board_logic.get_board_list(db=db)
    result = (str(i.name) for i in category_list)
    return result


async def get_category_list(
    *,
    db: AsyncSession,
    board: str,
) -> Iterable[str]:
    category_list = await board_logic.get_category_list(db=db, board=board)
    result = (str(i.name) for i in category_list)
    return result


async def get_parent_category(
    *,
    db: AsyncSession,
    category: str,
) -> str:
    parent = await board_logic.get_parent_category(db=db, category=category)
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no parent category",
        )
    result = board_response.Category.model_validate(obj=parent).name
    return result


async def get_post_list(
    *,
    db: AsyncSession,
    board: board_enum.BoardEnum,
    keyword: str,
    size: int,
    page: int,
) -> board_response.PostListResponse:
    category_entity = await board_logic.get_category_id(
        db=db,
        category=board,
    )

    count = await board_logic.get_post_count(
        db=db,
        category=category_entity.id,
        keyword=keyword,
    )

    post_list = await board_logic.get_post_list(
        db=db,
        board=category_entity.id,
        keyword=keyword,
        size=size,
        page=page,
    )
    response_list = (
        post_response.BoardPostResponse.model_validate(obj=x) for x in post_list
    )

    res = board_response.PostListResponse(total=count, post_list=response_list)
    return res


async def create_post(
    *,
    db: AsyncSession,
    user: user_request.UserCurrent,
    category: str,
    data: post_request.PostBaseRequset,
) -> None:
    category_entity = await board_logic.get_category_id(db=db, category=category)
    await board_logic.create_post(
        db=db,
        category=category_entity.id,
        user_id=user.id,
        title=data.title,
        content=data.content,
    )
