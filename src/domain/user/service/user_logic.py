from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.configs import KST, pwd_context
from src.db.query.user import user_create, user_update

from ..model import user_request


async def create_user(
    *,
    db: AsyncSession,
    data: user_request.UserCreateRequest,
) -> None:
    await user_create.create_user(
        db=db,
        name=data.name,
        password=pwd_context.hash(secret=data.password1),
        email=data.email,
        created_datetime=datetime.now(KST),
    )


async def update_user(
    *,
    db: AsyncSession,
    update_info: user_request.UserBase,
    current_user: user_request.UserCurrent,
) -> None:
    await user_update.update_user(
        db=db,
        user_id=current_user.id,
        name=update_info.name,
        email=update_info.email,
    )


async def update_password(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
    data: user_request.Password,
) -> None:
    await user_update.update_password(
        db=db,
        user_id=current_user.id,
        password=pwd_context.hash(secret=data.password1),
    )


async def delete_user(
    *,
    db: AsyncSession,
    user: user_request.UserCurrent,
) -> None:
    await user_update.resign_user(db=db, user_id=user.id)
