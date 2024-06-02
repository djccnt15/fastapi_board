from typing import Iterable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.comment.model import comment_request, comment_response
from src.domain.user.model import user_request

from ..converter import post_converter
from ..model import post_request, post_response
from ..service import post_logic, verify_logic, vote_logic


async def get_post(
    *,
    db: AsyncSession,
    post_id: int,
) -> post_response.PostResponse:
    post_entity = await post_logic.get_post(db=db, post_id=post_id)
    post = await post_converter.to_post_response(data=post_entity)
    return post


async def update_post(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
    data: post_request.PostUpdateRequest,
) -> None:
    await verify_logic.verify_author(db=db, current_user=current_user, post_id=post_id)
    await post_logic.update_post(
        db=db,
        title=data.title,
        content=data.content,
        post_id=post_id,
    )


async def delete_post(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
) -> None:
    await verify_logic.verify_author(db=db, current_user=current_user, post_id=post_id)
    await verify_logic.verify_comment(db=db, post_id=post_id)
    await post_logic.delete_post(db=db, post_id=post_id)


async def get_post_history(
    *,
    db: AsyncSession,
    post_id: int,
) -> Iterable[post_response.PostContentResponse]:
    history = await post_logic.get_post_history(db=db, post_id=post_id)
    result = (post_response.PostContentResponse.model_validate(v) for v in history)
    return result


async def vote_post(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
) -> None:
    try:
        # vote post
        await vote_logic.vote_post(db=db, current_user=current_user, post_id=post_id)
    except IntegrityError:
        # revoke vote post
        await vote_logic.revoke_vote_post(
            db=db,
            current_user=current_user,
            post_id=post_id,
        )


async def get_comment_list(
    *,
    db: AsyncSession,
    post_id: int,
) -> Iterable[comment_response.CommentResponse]:
    comment_list = await post_logic.get_comment_list(db=db, post_id=post_id)
    response_list = (
        comment_response.CommentResponse.model_validate(obj=v) for v in comment_list
    )
    return response_list


async def create_comment(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    post_id: int,
    data: comment_request.CommentCreateRequest,
) -> None:
    await post_logic.create_comment(
        db=db,
        user_id=current_user.id,
        post_id=post_id,
        content=data.content,
    )
