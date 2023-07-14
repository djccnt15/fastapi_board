from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from env.database import get_db
from src.crud import *
from src.schemas import *
from src.models import User
from src.app import get_current_user

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=SuccessCreate)
async def comment_create(
        id_post: UUID,
        comment: ContentBase,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    post = await get_post(db, id_post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=no_id
        )

    id_comment = uuid4()
    now = datetime.now()
    await create_comment(db, id_comment, post, now, current_user)
    await create_comment_detail(db, comment, id_comment, now)
    return SuccessCreate()


@router.put('/upd', response_model=SuccessUpdate)
async def comment_upd(
        id_comment: UUID,
        comment_content: ContentBase,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    comment = await get_comment(db, id_comment)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    elif comment.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=not_val_user
        )

    ver = await get_comment_ver(db, id_comment)
    await create_comment_detail(db, comment_content, id_comment, version=ver+1)
    return SuccessUpdate()


@router.delete('/del', response_model=SuccessDel)
async def comment_del(
        id_comment: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    comment = await get_comment(db, id_comment)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    elif comment.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=not_val_user
        )

    await del_comment(db, id_comment)
    return SuccessDel()


@router.get('/his', response_model=CommentHis)
async def comment_his(id_comment: UUID, db: AsyncSession = Depends(get_db)):
    comment_his = await get_comment_his(db, id_comment)
    return CommentHis(comment_his=comment_his)