from typing import Annotated, Iterable

from fastapi import APIRouter, Body, Path

from src import dependency
from src.core import auth
from src.core.model.enums import ResponseEnum
from src.domain.comment.model.comment_response import CommentContentResponse

from ..business import comment_process
from ..model import comment_request

router = APIRouter(prefix="/comment")


@router.put(path="/{id}")
async def update_comment(
    current_user: auth.CurrentUser,
    repo: dependency.CommentRepo,
    body: Annotated[comment_request.CommentCreateRequest, Body()],
    id: Annotated[int, Path(gt=0)],
) -> ResponseEnum:
    await comment_process.update_comment(
        user=current_user,
        repo=repo,
        comment_id=id,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.delete(path="/{id}")
async def delete_comment(
    current_user: auth.CurrentUser,
    repo: dependency.CommentRepo,
    id: Annotated[int, Path(gt=0)],
) -> ResponseEnum:
    await comment_process.delete_comment(user=current_user, repo=repo, comment_id=id)
    return ResponseEnum.DELETE


@router.get(path="/{id}/history")
async def get_comment_history(
    repo: dependency.CommentRepo,
    id: Annotated[int, Path(gt=0)],
) -> Iterable[CommentContentResponse]:
    res = await comment_process.get_comment_history(repo=repo, comment_id=id)
    return res


@router.post(path="/{id}/vote")
async def vote_comment(
    current_user: auth.CurrentUser,
    repo: dependency.CommentRepo,
    id: Annotated[int, Path(gt=0)],
) -> ResponseEnum:
    await comment_process.vote_comment(repo=repo, user=current_user, comment_id=id)
    return ResponseEnum.VOTE
