from typing import Iterable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import get_current_user
from src.core.model.enums import ResponseEnum
from src.db.database import get_db
from src.domain.comment.model.comment_response import CommentContentResponse
from src.domain.user.model import user_request

from ..business import comment_process
from ..model import comment_request

router = APIRouter(prefix="/comment")


@router.put(path="/{id}")
async def update_comment(
    id: int,
    body: comment_request.CommentCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await comment_process.update_comment(
        db=db,
        current_user=current_user,
        comment_id=id,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.delete(path="/{id}")
async def delete_comment(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await comment_process.delete_comment(
        db=db,
        current_user=current_user,
        comment_id=id,
    )
    return ResponseEnum.DELETE


@router.get(path="/{id}/history")
async def get_comment_history(
    id: int,
    db: AsyncSession = Depends(get_db),
) -> Iterable[CommentContentResponse]:
    res = await comment_process.get_comment_history(db=db, comment_id=id)
    return res


@router.post(path="/{id}/vote")
async def vote_comment(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await comment_process.vote_comment(db=db, current_user=current_user, comment_id=id)
    return ResponseEnum.VOTE
