from datetime import datetime

from src.core import configs, security
from src.dependency import ports

from ..model import user_request


async def create_user(
    *,
    repo: ports.UserRepository,
    data: user_request.UserCreateRequest,
) -> None:
    await repo.create_user(
        name=data.name,
        password=security.pwd_context.hash(secret=data.password1),
        email=data.email,
        created_datetime=datetime.now(configs.KST),
    )


async def update_user(
    *,
    repo: ports.UserRepository,
    data: user_request.UserBase,
    current_user: user_request.UserCurrent,
) -> None:
    await repo.update_user(user_id=current_user.id, name=data.name, email=data.email)


async def update_password(
    *,
    repo: ports.UserRepository,
    user: user_request.UserCurrent,
    data: user_request.Password,
) -> None:
    await repo.update_password(
        user_id=user.id,
        password=security.pwd_context.hash(secret=data.password1),
    )


async def delete_user(
    *,
    repo: ports.UserRepository,
    user: user_request.UserCurrent,
) -> None:
    await repo.resign_user(user_id=user.id)
