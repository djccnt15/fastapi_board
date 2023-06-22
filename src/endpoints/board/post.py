from uuid import UUID, uuid4
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import get_db
from src.crud.board import *
from src.schemas import Tags, CreateSuccess, PostList, PostDetailList, no_id, CategoryEnum
from src.models import User
from src.app import get_current_user

router = APIRouter(
    prefix='/api/board',
)


@router.post(
        '/post/create',
        tags=[Tags.board],
        status_code=status.HTTP_201_CREATED,
        response_model=CreateSuccess
)
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
    return CreateSuccess()


@router.get('/list/{category}', tags=[Tags.board], response_model=PostList)
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


@router.get('/post', tags=[Tags.board], response_model=PostDetailList)
async def post_detail(id: UUID, db: AsyncSession = Depends(get_db)):
    post = await get_post(db, id)
    comment = await get_comment_list(db, id)
    if post is None or comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=no_id
        )
    return PostDetailList(post=post, comment=comment)