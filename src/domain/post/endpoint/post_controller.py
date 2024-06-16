from typing import Annotated, Iterable

from fastapi import APIRouter, Body, Path
from fastapi.responses import Response
from starlette import status

from src import dependency
from src.core import auth
from src.core.model.enums import ResponseEnum
from src.domain.comment.model import comment_request, comment_response

from ..business import post_process
from ..model import post_request, post_response

router = APIRouter(prefix="/post")


@router.get(path="/{id}")
async def get_post(
    repo: dependency.PostRepo,
    cache: dependency.CacheRepo,
    id: Annotated[int, Path(gt=0)],
) -> post_response.PostResponse:
    res = await post_process.get_post(repo=repo, cache=cache, post_id=id)
    return res


@router.put(path="/{id}")
async def update_post(
    current_user: auth.CurrentUser,
    repo: dependency.PostRepo,
    cache: dependency.CacheRepo,
    id: Annotated[int, Path(gt=0)],
    body: Annotated[post_request.PostUpdateRequest, Body()],
) -> ResponseEnum:
    await post_process.update_post(
        user=current_user,
        repo=repo,
        cache=cache,
        post_id=id,
        data=body,
    )
    return ResponseEnum.UPDATE


@router.delete(path="/{id}")
async def delete_post(
    current_user: auth.CurrentUser,
    post_repo: dependency.PostRepo,
    comment_repo: dependency.CommentRepo,
    cache: dependency.CacheRepo,
    id: Annotated[int, Path(gt=0)],
) -> ResponseEnum:
    await post_process.delete_post(
        user=current_user,
        post_repo=post_repo,
        comment_repo=comment_repo,
        cache=cache,
        post_id=id,
    )
    return ResponseEnum.DELETE


@router.get(path="/{id}/history")
async def get_post_history(
    repo: dependency.PostRepo,
    id: Annotated[int, Path(gt=0)],
) -> Iterable[post_response.PostContentResponse]:
    res = await post_process.get_post_history(repo=repo, post_id=id)
    return res


@router.get(path="/{id}/download")
async def download_post_history(
    repo: dependency.PostRepo,
    id: Annotated[int, Path(gt=0)],
) -> Response:
    res = await post_process.download_post_history(repo=repo, post_id=id)
    return res


@router.post(path="/{id}/vote")
async def vote_post(
    current_user: auth.CurrentUser,
    repo: dependency.PostRepo,
    id: Annotated[int, Path(gt=0)],
) -> ResponseEnum:
    await post_process.vote_post(repo=repo, user=current_user, post_id=id)
    return ResponseEnum.VOTE


@router.get(path="/{id}/comment")
async def get_post_comment(
    repo: dependency.CommentRepo,
    id: Annotated[int, Path(gt=0)],
) -> Iterable[comment_response.CommentResponse]:
    res = await post_process.get_comment_list(repo=repo, post_id=id)
    return res


@router.post(path="/{id}/comment", status_code=status.HTTP_201_CREATED)
async def create_comment(
    current_user: auth.CurrentUser,
    repo: dependency.CommentRepo,
    id: Annotated[int, Path(gt=0)],
    body: Annotated[comment_request.CommentCreateRequest, Body()],
) -> ResponseEnum:
    await post_process.create_comment(
        user=current_user,
        repo=repo,
        post_id=id,
        data=body,
    )
    return ResponseEnum.CREATE
