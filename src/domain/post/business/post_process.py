from datetime import datetime
from typing import Iterable

from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError

from src.caching.enums.cache_enum import CacheKeyEnum
from src.caching.model import post_redis
from src.dependency import ports
from src.domain.comment.model import comment_request, comment_response
from src.domain.user.model import user_request

from ..converter import post_converter
from ..model import post_request, post_response
from ..service import post_logic, verify_logic, vote_logic


async def get_post(
    *,
    repo: ports.PostRepository,
    cache: ports.CacheRepository,
    post_id: int,
) -> post_response.PostResponse:
    cache_key = CacheKeyEnum.POST_KEY % post_id
    post_cache = await cache.read_map_cache(key=cache_key)
    if post_cache:
        cache_model = post_redis.PostRedisModel.model_validate(obj=post_cache)
        post = await post_converter.redis_to_post_response(data=cache_model)
        return post

    post_entity = await post_logic.get_post(repo=repo, post_id=post_id)
    post = await post_converter.to_post_response(data=post_entity)

    post_model = await post_converter.to_post_redis(data=post)
    await cache.create_map_cache(key=cache_key, data=post_model.model_dump())
    return post


async def update_post(
    *,
    user: user_request.UserCurrent,
    repo: ports.PostRepository,
    cache: ports.CacheRepository,
    post_id: int,
    data: post_request.PostUpdateRequest,
) -> None:
    await verify_logic.verify_author(repo=repo, user=user, post_id=post_id)
    await post_logic.update_post(
        repo=repo,
        title=data.title,
        content=data.content,
        post_id=post_id,
    )
    await cache.delete_cache(key=CacheKeyEnum.POST_KEY % post_id)


async def delete_post(
    *,
    user: user_request.UserCurrent,
    post_repo: ports.PostRepository,
    comment_repo: ports.CommentRepository,
    cache: ports.CacheRepository,
    post_id: int,
) -> None:
    await verify_logic.verify_author(repo=post_repo, user=user, post_id=post_id)
    await verify_logic.verify_comment(repo=comment_repo, post_id=post_id)
    await post_logic.delete_post(repo=post_repo, post_id=post_id)
    await cache.delete_cache(key=CacheKeyEnum.POST_KEY % post_id)


async def get_post_history(
    *,
    repo: ports.PostRepository,
    post_id: int,
) -> Iterable[post_response.PostContentResponse]:
    history = await post_logic.get_post_history(repo=repo, post_id=post_id)
    result = (post_response.PostContentResponse.model_validate(v) for v in history)
    return result


async def download_post_history(
    *,
    repo: ports.PostRepository,
    post_id: int,
) -> Response:
    history = await post_logic.get_post_history(repo=repo, post_id=post_id)
    rows = (post_response.PostContentResponse.model_validate(v) for v in history)
    data = await post_logic.create_post_history_data(data=rows)
    res = Response(content=data, media_type="text/csv")
    now = datetime.now().replace(microsecond=0)
    file_name = f"POST_HISTORY_{post_id}_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    res.headers["Content-Disposition"] = f"attachment; filename={file_name}"
    return res


async def vote_post(
    *,
    user: user_request.UserCurrent,
    repo: ports.PostRepository,
    post_id: int,
) -> None:
    try:
        # vote post
        await vote_logic.vote_post(repo=repo, user=user, post_id=post_id)
    except IntegrityError:
        # revoke vote post
        await vote_logic.revoke_vote_post(repo=repo, user=user, post_id=post_id)


async def get_comment_list(
    *,
    repo: ports.CommentRepository,
    post_id: int,
) -> Iterable[comment_response.CommentResponse]:
    comment_list = await post_logic.get_comment_list(repo=repo, post_id=post_id)
    response_list = (
        comment_response.CommentResponse.model_validate(obj=v) for v in comment_list
    )
    return response_list


async def create_comment(
    *,
    user: user_request.UserCurrent,
    repo: ports.CommentRepository,
    post_id: int,
    data: comment_request.CommentCreateRequest,
) -> None:
    await post_logic.create_comment(
        repo=repo,
        user_id=user.id,
        post_id=post_id,
        content=data.content,
    )
