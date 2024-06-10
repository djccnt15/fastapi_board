from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.caching.enums.redis_enum import RedisKeyEnum

from ..model import user_request, user_response
from ..service import login_logic, user_logic, verify_logic


async def create_user(
    *,
    db: AsyncSession,
    data: user_request.UserCreateRequest,
) -> None:
    await verify_logic.verify_user_create(db=db, data=data)
    await user_logic.create_user(db=db, data=data)


async def login_user(
    *,
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
) -> user_response.Token:
    user = await login_logic.identify_user(db=db, form_data=form_data)
    current_user = user_request.UserCurrent.model_validate(obj=user)
    await login_logic.create_login_log(db=db, user_id=current_user.id)
    token = await login_logic.create_access_token(username=current_user.name)
    return token


async def update_user(
    *,
    db: AsyncSession,
    redis: Redis,
    current_user: user_request.UserCurrent,
    data: user_request.UserBase,
) -> None:
    await verify_logic.verify_user_update(db=db, data=current_user)
    await user_logic.update_user(
        db=db,
        data=data,
        current_user=current_user,
    )
    await redis.delete(RedisKeyEnum.USER_KEY % current_user.name)


async def update_password(
    *,
    db: AsyncSession,
    redis: Redis,
    current_user: user_request.UserCurrent,
    data: user_request.Password,
) -> None:
    await user_logic.update_password(
        db=db,
        current_user=current_user,
        data=data,
    )
    await redis.delete(RedisKeyEnum.USER_KEY % current_user.name)


async def resign_user(
    *,
    db: AsyncSession,
    redis: Redis,
    current_user: user_request.UserCurrent,
) -> None:
    await user_logic.delete_user(db=db, user=current_user)
    await redis.delete(RedisKeyEnum.USER_KEY % current_user.name)
