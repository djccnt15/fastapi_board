from datetime import datetime

from src.caching.model import user_redis
from src.db.entity.user_entity import UserEntity


async def to_user_entity(*, user_model: user_redis.UserRedisModel) -> UserEntity:
    user_data = user_model.model_dump()
    user_data["created_datetime"] = datetime.fromisoformat(user_model.created_datetime)
    user_entity = UserEntity(**user_data)
    return user_entity


async def to_user_redis(*, user_entity: UserEntity) -> user_redis.UserRedisModel:
    user_data = vars(user_entity)
    user_data["created_datetime"] = user_entity.created_datetime.isoformat()
    user = user_redis.UserRedisModel.model_validate(obj=user_data)
    return user
