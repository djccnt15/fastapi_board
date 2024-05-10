from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db

from ..business import board_process
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
