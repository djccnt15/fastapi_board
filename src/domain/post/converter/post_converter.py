from datetime import datetime

from src.caching.model import post_redis

from ..model import post_response


async def to_post_response(*, data: dict) -> post_response.PostResponse:
    post_entity = vars(data.get("PostEntity"))

    post_id = post_entity.get("id", None)
    created_datetime = post_entity.get("created_datetime", None)
    updated_datetime = data.get("created_datetime", None)
    category = vars(data.get("PostCategoryEntity")).get("name", None)
    user = vars(data.get("UserEntity")).get("name", None)
    title = data.get("title", None)
    content = data.get("content", None)

    res = post_response.PostResponse(
        id=post_id,
        created_datetime=created_datetime,
        updated_datetime=updated_datetime,
        category=category,
        user=user,
        title=title,
        content=content,
    )
    return res


async def to_post_redis(
    *,
    data: post_response.PostResponse,
) -> post_redis.PostRedisModel:
    post_data = data.model_dump()
    post_data["created_datetime"] = data.created_datetime.isoformat()
    post_data["updated_datetime"] = data.updated_datetime.isoformat()
    post = post_redis.PostRedisModel.model_validate(obj=post_data)
    return post


async def redis_to_post_response(
    *,
    data: post_redis.PostRedisModel,
) -> post_response.PostResponse:
    post_data = data.model_dump()
    post_data["created_datetime"] = datetime.fromisoformat(data.created_datetime)
    post_data["updated_datetime"] = datetime.fromisoformat(data.updated_datetime)
    post = post_response.PostResponse.model_validate(obj=post_data)
    return post
