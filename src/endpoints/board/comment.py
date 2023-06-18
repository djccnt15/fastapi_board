from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings.database import get_db
from src.crud import get_post, create_comment, create_comment_detail
from src.schemas import CreateSuccess, no_id, CommentCreate
from src.models import User
from src.app import get_current_user

router = APIRouter(
    prefix='/api/board/comment',
)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CreateSuccess)
async def comment_create(
        id: UUID,
        comment: CommentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
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