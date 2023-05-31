from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from settings.database import get_db
from src.crud.board.post import *
from src.crud.board.comment import *
from src.schemas.board.post import *
from src.schemas.board.comment import *

router = APIRouter(
    prefix="/api/board",
)


@router.get("/{category}", response_model=PostList)
def post_list(category: str, db: Session = Depends(get_db)):
    total, post_list = get_post_list(db, category)
    if total == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such category"
        )
    return {
        'total': total,
        'post_list': post_list
    }


@router.get("/post/", response_model=PostDetailList)
def post_detail(id: UUID, db: Session = Depends(get_db)):
    post = get_post(db, id)
    comment = get_comment_list(db, id)
    if post is None or comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such ID"
        )
    return {
        'post': post,
        'comment': comment
    }