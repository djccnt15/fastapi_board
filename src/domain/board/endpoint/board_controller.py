from typing import Annotated, Iterable

from fastapi import APIRouter, Body, Path, Query
from starlette import status

from src import dependency
from src.core import auth
from src.core.model.enums import ResponseEnum
from src.domain.post.model import post_request

from ..business import board_process
from ..model import board_response
from ..model.enums import board_enum

router = APIRouter(prefix="/board")


@router.get(path="")
async def board_list(repo: dependency.CategoryRepo) -> Iterable[str]:
    board_list = await board_process.get_board_list(repo=repo)
    return board_list


@router.get(path="/category")
async def get_category(
    repo: dependency.CategoryRepo,
    board: Annotated[board_enum.BoardEnum, Query()],
) -> Iterable[str]:
    category_list = await board_process.get_category_list(repo=repo, board=board)
    return category_list


@router.get(path="/parent")
async def get_parent(
    repo: dependency.CategoryRepo,
    category: Annotated[board_enum.CategoryEnum, Query()],
) -> str:
    parent = await board_process.get_parent_category(repo=repo, category=category)
    return parent


@router.get(path="/{board}")
async def get_post_list(
    category_repo: dependency.CategoryRepo,
    post_repo: dependency.PostRepo,
    board: Annotated[board_enum.BoardEnum, Path()],
    keyword: Annotated[str | None, Query()] = None,
    size: Annotated[int, Query(gt=0)] = 10,
    page: Annotated[int, Query(ge=0)] = 0,
) -> board_response.PostListResponse:
    res = await board_process.get_post_list(
        category_repo=category_repo,
        post_repo=post_repo,
        board=board,
        keyword=keyword,
        size=size,
        page=page,
    )
    return res


@router.post(path="/{category}", status_code=status.HTTP_201_CREATED)
async def create_post(
    current_user: auth.CurrentUser,
    category_repo: dependency.CategoryRepo,
    post_repo: dependency.PostRepo,
    category: Annotated[board_enum.CategoryEnum, Path()],
    body: Annotated[post_request.PostBaseRequset, Body()],
) -> ResponseEnum:
    await board_process.create_post(
        category_repo=category_repo,
        post_repo=post_repo,
        user=current_user,
        category=category,
        data=body,
    )
    return ResponseEnum.CREATE
