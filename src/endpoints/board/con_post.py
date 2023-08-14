from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from common.database import get_db
from src.crud import *
from src.schemas import *
from src.models import User
from src.app import get_current_user

router = APIRouter()


@router.get('/boards', response_model=list)
async def board_list(db: AsyncSession = Depends(get_db)):
    board_list = await read_category_t1_list(db)
    return [i.category for i in board_list]


@router.get('/categories', response_model=list)
async def category_list(category: CategoryEnum, db: AsyncSession = Depends(get_db)):
    category_list = await read_category_list(db, category.name)
    return [i.category for i in category_list]


@router.get('/category', response_model=CategoryBase)
async def category_parent(category: str, db: AsyncSession = Depends(get_db)):
    category_upper = await get_category_parent(db, category)
    if category_upper is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no parent category'
        )
    return CategoryBase.from_orm(category_upper)


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


@router.get('/post/detail', response_model=PostDetail)
async def post_detail(id_post: UUID, db: AsyncSession = Depends(get_db)):
    post_detail = await get_post_detail(db, id_post)
    comment_list = await get_comment_list(db, id_post)
    if post_detail is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    return PostDetail(post_detail=post_detail, comment_list=comment_list)


@router.put('/post/upd', response_model=SuccessUpdate)
async def post_update(
        id_post: UUID,
        post_content: PostCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    post = await get_post(db, id_post)
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

    ver = await get_post_ver(db, id_post)
    await create_post_detail(db, post_content, id_post, version=ver+1)
    return SuccessUpdate()


@router.delete('/post/del', response_model=SuccessDel)
async def post_del(
        id_post: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    post = await get_post(db, id_post)
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
    elif await get_commented_post(db, id_post):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can't delete commented post"
        )

    await del_post(db, id_post)
    return SuccessDel()


@router.get('/post/his', response_model=PostHis)
async def post_his(id_post: UUID, db: AsyncSession = Depends(get_db)):
    post_his = await get_post_his(db, id_post)
    return PostHis(post_his=post_his)


@router.post('/post/vote', status_code=status.HTTP_204_NO_CONTENT)
async def post_vote(
        id_post: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    post = await get_post(db, id_post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    try:
        await vote_post(db, id_post, current_user)
    except SQLAlchemyError:
        await vote_post_revoke(db, id_post, current_user)