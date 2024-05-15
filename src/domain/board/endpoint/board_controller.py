from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.auth import get_current_user
from src.common.model.enums import ResponseEnum
from src.db.database import get_db
from src.domain.post.model import post_request
from src.domain.user.model import user_request

from ..business import board_process
from ..model import board_response
from ..model.enums import board_enum

router = APIRouter(prefix="/board")


@router.get(path="")
async def board_list(
    db: AsyncSession = Depends(get_db),
) -> Iterable[str]:
    board_list = await board_process.get_board_list(db=db)
    return board_list


@router.get(path="/category")
async def get_list(
    board: board_enum.BoardEnum,
    db: AsyncSession = Depends(get_db),
) -> Iterable[str]:
    category_list = await board_process.get_category_list(db=db, board=board)
    return category_list


@router.get(path="/parent")
async def get_parent(
    category: board_enum.CategoryEnum,
    db: AsyncSession = Depends(get_db),
) -> str:
    parent = await board_process.get_parent_category(db=db, category=category)
    return parent


@router.get(path="/{board}")
async def get_post_list(
    board: board_enum.BoardEnum,
    keyword: str = "",
    size: int = 10,
    page: int = 0,
    db: AsyncSession = Depends(get_db),
) -> board_response.PostListResponse:
    res = await board_process.get_post_list(
        db=db,
        board=board,
        keyword=keyword,
        size=size,
        page=page,
    )
    return res


@router.post(path="/{category}")
async def create_post(
    category: board_enum.CategoryEnum,
    request: post_request.PostBaseRequset,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await board_process.create_post(
        db=db,
        user=current_user,
        category=category,
        data=request,
    )
    return ResponseEnum.CREATE
