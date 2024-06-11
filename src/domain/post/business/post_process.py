from pathlib import Path
from typing import Iterable

from redis.asyncio.client import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.caching.command import redis_cmd
from src.caching.enums.redis_enum import RedisKeyEnum
from src.caching.model import post_redis
from src.domain.comment.model import comment_request, comment_response
from src.domain.user.model import user_request

from ..converter import post_converter
from ..model import post_request, post_response
from ..service import post_logic, verify_logic, vote_logic


async def get_post(
    *,
    db: AsyncSession,
    redis: Redis,
    post_id: int,
) -> post_response.PostResponse:
    redis_key = RedisKeyEnum.POST_KEY % post_id
    redis_data = await redis.hgetall(name=redis_key)  # type: ignore
    if redis_data:
        redis_model = post_redis.PostRedisModel.model_validate(obj=redis_data)
        redis_post = await post_converter.redis_to_post_response(data=redis_model)
        return redis_post

    post_entity = await post_logic.get_post(db=db, post_id=post_id)
    post = await post_converter.to_post_response(data=post_entity)

    post_model = await post_converter.to_post_redis(data=post)
    await redis_cmd.create_expire_hset(
        redis_key=redis_key,
        time=30,
        data=post_model.model_dump(),
    )

    return post


async def update_post(
    *,
    db: AsyncSession,
    redis: Redis,
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
    await redis.delete(RedisKeyEnum.POST_KEY % post_id)


async def delete_post(
    *,
    db: AsyncSession,
    redis: Redis,
    current_user: user_request.UserCurrent,
    post_id: int,
) -> None:
    await verify_logic.verify_author(db=db, current_user=current_user, post_id=post_id)
    await verify_logic.verify_comment(db=db, post_id=post_id)
    await post_logic.delete_post(db=db, post_id=post_id)
    await redis.delete(RedisKeyEnum.POST_KEY % post_id)


async def get_post_history(
    *,
    db: AsyncSession,
    post_id: int,
) -> Iterable[post_response.PostContentResponse]:
    history = await post_logic.get_post_history(db=db, post_id=post_id)
    result = (post_response.PostContentResponse.model_validate(v) for v in history)
    return result


async def download_post_history(
    *,
    db: AsyncSession,
    post_id: int,
) -> Path:
    history = await post_logic.get_post_history(db=db, post_id=post_id)
    rows = (post_response.PostContentResponse.model_validate(v) for v in history)
    file_path = await post_logic.create_post_history_file(data=rows, post_id=post_id)
    return file_path


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
