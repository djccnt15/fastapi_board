from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from settings.database import get_db
from src.crud.board.post import get_post
from src.crud.board.comment import create_comment, create_comment_detail
from src.schemas.common.common import CreateSuccess, no_id
from src.schemas.board.comment import CommentCreate
from src.models import User as UserDao
from src.app.auth import get_current_user

router = APIRouter(
    prefix='/api/board/comment',
)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CreateSuccess)
async def comment_create(
        id: UUID,
        comment: CommentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: UserDao = Depends(get_current_user)
):
    post = await get_post(db, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=no_id
        )

    post = post._asdict()['Post']
    id_comment = uuid4()
    now = datetime.now()
    await create_comment(db, id_comment, post, now, current_user)
    await create_comment_detail(db, comment, id_comment, now)
    return CreateSuccess()