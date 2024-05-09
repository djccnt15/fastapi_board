from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exception import NotUniqueError
from src.db.query import user_crud

from ..model import user_request


async def verify_user(
    *,
    db: AsyncSession,
    user: user_request.UserCurrent,
) -> None:
    user_list = await user_crud.read_user_by_name_email(
        db=db,
        name=user.name,
        email=user.email,
    )

    email_conflict = [u for u in user_list if user.email == u.email and user.id != u.id]
    if email_conflict:
        raise NotUniqueError(field=user.email)

    name_conflict = [u for u in user_list if user.name == u.name and user.id != u.id]
    if name_conflict:
        raise NotUniqueError(field=user.name)


async def update_user(
    *,
    db: AsyncSession,
    update_info: user_request.UserBase,
    current_user: user_request.UserCurrent,
) -> None:
    await user_crud.update_user(
        db=db,
        user_id=current_user.id,
        name=update_info.name,
        email=update_info.email,
    )
