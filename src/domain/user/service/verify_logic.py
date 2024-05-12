from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exception import NotUniqueError
from src.db.query.user import user_read

from ..model import user_request


async def verify_user_info(
    *,
    db: AsyncSession,
    user: user_request.UserCreateRequest,
) -> None:
    user_list = await user_read.read_user_by_name_email(
        db=db,
        name=user.name,
        email=user.email,
    )

    username_conflict = [u for u in user_list if user.name == u.name]
    if username_conflict:
        raise NotUniqueError(field=user.name)

    email_conflict = [u for u in user_list if user.email == u.email]
    if email_conflict:
        raise NotUniqueError(field=user.email)


async def verify_user(
    *,
    db: AsyncSession,
    user: user_request.UserCurrent,
) -> None:
    user_list = await user_read.read_user_by_name_email(
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
