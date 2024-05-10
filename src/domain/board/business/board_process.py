from typing import Iterable

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..model import board_response
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
