from sqlalchemy.ext.asyncio import AsyncSession

from src.db.query.user import user_delete

from ..model import user_request


async def delete_user(
    *,
    db: AsyncSession,
    user: user_request.UserCurrent,
) -> None:
    await user_delete.delete_user(db=db, user_id=user.id)
