from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.caching import redis_db
from src.caching.command import redis_cmd
from src.caching.enums.redis_enum import RedisKeyEnum
from src.caching.model import user_redis
from src.core import configs
from src.db import database
from src.db.entity.user_entity import RoleEntity, UserEntity
from src.db.query.user import user_read
from src.domain.user.converter import user_converter
from src.domain.user.model.enums import user_enum

config = configs.config.fastapi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


async def verify_user_state(*, user: UserEntity):
    for state in user.state:
        if str(state.name) == user_enum.UserStateEnum.BLOCKED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="you are blocked",
            )
        elif str(state.name) == user_enum.UserStateEnum.INACTIVATE:
            # TODO
            ...


async def verify_admin(*, role: RoleEntity) -> bool:
    if role.name == user_enum.UserRoleEnum.ADMIN:
        return True
    return False


async def get_current_user(
    *,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(database.get_db),
    redis: Redis = Depends(redis_db.get_redis),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token,
            key=config.auth.secret_key,
            algorithms=config.auth.algorithm,
        )
        username = str(payload.get("sub"))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        redis_key = RedisKeyEnum.USER_KEY % username
        redis_data = await redis.hgetall(name=redis_key)  # type: ignore
        if redis_data:
            redis_user = user_redis.UserRedisModel.model_validate(obj=redis_data)
            user_entity = await user_converter.to_user_entity(user_model=redis_user)
            return user_entity

        user_entity = await user_read.read_user_by_name(db=db, name=username)
        if user_entity is None:
            raise credentials_exception
        await verify_user_state(user=user_entity)

        user_model = await user_converter.to_user_redis(user_entity=user_entity)
        await redis_cmd.create_expire_hset(
            redis_key=redis_key,
            time=600,
            data=user_model.model_dump(),
        )

        return user_entity
