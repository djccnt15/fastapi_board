from typing import Iterable

from fastapi import HTTPException
from starlette import status

from src import dependency
from src.domain.post.model import post_request, post_response
from src.domain.user.model import user_request

from ..model import board_response
from ..model.enums import board_enum
from ..service import board_logic


async def get_board_list(*, repo: dependency.CategoryRepo) -> Iterable[str]:
    category_list = await board_logic.get_board_list(repo=repo)
    result = (i.name for i in category_list)
    return result


async def get_category_list(
    *,
    repo: dependency.CategoryRepo,
    board: str,
) -> Iterable[str]:
    category_list = await board_logic.get_category_list(repo=repo, board=board)
    result = (i.name for i in category_list)
    return result


async def get_parent_category(
    *,
    repo: dependency.CategoryRepo,
    category: str,
) -> str:
    parent = await board_logic.get_parent_category(repo=repo, category=category)
    if parent is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no parent category",
        )
    result = board_response.Category.model_validate(obj=parent).name
    return result


async def get_post_list(
    *,
    category_repo: dependency.CategoryRepo,
    post_repo: dependency.PostRepo,
    board: board_enum.BoardEnum,
    keyword: str,
    size: int,
    page: int,
) -> board_response.PostListResponse:
    category_entity = await board_logic.get_category_id(
        repo=category_repo,
        category=board,
    )

    kw = f"%{keyword}%"
    count = await board_logic.get_post_count(
        repo=post_repo,
        category=category_entity.id,
        keyword=kw,
    )
    post_list = await board_logic.get_post_list(
        repo=post_repo,
        board=category_entity.id,
        keyword=kw,
        size=size,
        page=page,
    )
    response_list = (
        post_response.BoardPostResponse.model_validate(obj=v) for v in post_list
    )

    res = board_response.PostListResponse(total=count, post_list=response_list)
    return res


async def create_post(
    *,
    category_repo: dependency.CategoryRepo,
    post_repo: dependency.PostRepo,
    user: user_request.UserCurrent,
    category: str,
    data: post_request.PostBaseRequset,
) -> None:
    category_entity = await board_logic.get_category_id(
        repo=category_repo,
        category=category,
    )
    await board_logic.create_post(
        repo=post_repo,
        category=category_entity.id,
        user_id=user.id,
        title=data.title,
        content=data.content,
    )
