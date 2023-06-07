from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import get_db
from src.crud.board.post import *
from src.crud.board.comment import *
from src.schemas.board.post import *
from src.schemas.board.comment import *

router = APIRouter(
    prefix="/api/board",
)


@router.get("/{category}", response_model=PostList)
async def post_list(
    category: str,
    keyword: str = '',
    page: int = 0,
    size: int = 10,
    db: AsyncSession = Depends(get_db)
):
    total, post_list = await get_post_list(db, category, keyword, page * size, size)
    if total == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query Result is Empty"
        )
    return {
        'total': total,
        'post_list': post_list
    }


@router.get("/post/", response_model=PostDetailList)
async def post_detail(id: UUID, db: AsyncSession = Depends(get_db)):
    post = await get_post(db, id)
    comment = await get_comment_list(db, id)
    if post is None or comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such ID"
        )
    return {
        'post': post,
        'comment': comment
    }