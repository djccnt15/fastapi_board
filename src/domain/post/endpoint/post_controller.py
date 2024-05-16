from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.common.auth import get_current_user
from src.common.model.enums import ResponseEnum
from src.db.database import get_db
from src.domain.comment.model import comment_request, comment_response
from src.domain.user.model import user_request

from ..business import post_process
from ..model import post_request, post_response

router = APIRouter(prefix="/post")


@router.get(path="/{id}")
async def get_post(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> post_response.PostResponse:
    res = await post_process.get_post(db=db, post_id=id)
    return res


@router.put(path="/{id}")
async def update_post(
    id: int,
    request: post_request.PostCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await post_process.update_post(
        db=db,
        post_id=id,
        current_user=current_user,
        data=request,
    )
    return ResponseEnum.UPDATE


@router.delete(path="/{id}")
async def delete_post(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await post_process.delete_post(
        db=db,
        current_user=current_user,
        post_id=id,
    )
    return ResponseEnum.DELETE


@router.get(path="/{id}/history")
async def get_post_history(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Iterable[post_response.PostContentResponse]:
    res = await post_process.get_post_history(db=db, post_id=id)
    return res


@router.post(path="/{id}/vote")
async def vote_post(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await post_process.vote_post(
        db=db,
        current_user=current_user,
        post_id=id,
    )
    return ResponseEnum.VOTE


@router.get(path="/{id}/comment")
async def get_post_comment(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Iterable[comment_response.CommentResponse]:
    res = await post_process.get_comment_list(db=db, post_id=id)
    return res


@router.post(path="/{id}/comment", status_code=status.HTTP_201_CREATED)
async def create_comment(
    request: comment_request.CommentCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await post_process.create_comment(
        db=db,
        current_user=current_user,
        request=request,
    )
    return ResponseEnum.CREATE
