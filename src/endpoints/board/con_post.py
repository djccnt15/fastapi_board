from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import get_db
from src.crud import *
from src.schemas import *
from src.models import User
from src.app import get_current_user

router = APIRouter()


@router.get('/list', response_model=list)
async def board_list(db: AsyncSession = Depends(get_db)):
    board_list = await read_category_t1_list(db)
    return [i.category for i in board_list]


@router.get('/category/list', response_model=list)
async def category_list(category: CategoryEnum, db: AsyncSession = Depends(get_db)):
    category_list = await read_category_list(db, category.name)
    return [i.category for i in category_list]


@router.post('/post/create', status_code=status.HTTP_201_CREATED, response_model=SuccessCreate)
async def post_create(
        post: PostCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    category = await get_category_id(db, post.category)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no such category'
        )

    now = datetime.now()
    id_post = uuid4()
    await create_post(db, id_post, category.id, current_user, now)
    await create_post_detail(db, post, id_post, now)
    return SuccessCreate()


@router.get('/list/{category}', response_model=PostList)
async def post_list(
        category: CategoryEnum,
        keyword: str = '',
        page: int = 0,
        size: int = 10,
        db: AsyncSession = Depends(get_db)
):
    total, post_list = await get_post_list(db, category.name, keyword, page * size, size)
    if total == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Query Result is Empty'
        )
    return PostList(total=total, post_list=post_list)


@router.get('/post', response_model=PostDetailList)
async def post_detail(id: UUID, db: AsyncSession = Depends(get_db)):
    post_detail = await get_post_detail(db, id)
    comment_list = await get_comment_list(db, id)
    if post_detail is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    return PostDetailList(post_detail=post_detail, comment_list=comment_list)


@router.put('/update', response_model=SuccessUpdate)
async def post_update(
        id: UUID,
        post_content: PostContentBase,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    post = await get_post(db, id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    elif post.id_user != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=not_val_user
        )

    ver: int = await get_content_ver(db, id)
    await update_post(db, id, ver + 1, post_content)
    return SuccessUpdate()