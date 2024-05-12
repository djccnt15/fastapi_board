from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..model import user_request, user_response
from ..service import login_logic, user_logic, verify_logic


async def create_user(
    *,
    db: AsyncSession,
    request: user_request.UserCreateRequest,
) -> None:
    await verify_logic.verify_user_info(db=db, user=request)
    await user_logic.create_user(db=db, data=request)


async def login_user(
    *,
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm,
) -> user_response.Token:
    user = await login_logic.identify_user(db=db, form_data=form_data)
    current_user = user_request.UserCurrent.model_validate(obj=user)
    await login_logic.create_login_history(db=db, user_id=current_user.id)
    token = await login_logic.create_access_token(username=current_user.name)
    return token


async def update_user(
    *,
    db: AsyncSession,
    request: user_request.UserBase,
    current_user: user_request.UserCurrent,
) -> None:
    await verify_logic.verify_user(db=db, user=current_user)
    await user_logic.update_user(
        db=db,
        update_info=request,
        current_user=current_user,
    )


async def resign_user(
    *,
    db: AsyncSession,
    current_user: user_request.UserCurrent,
) -> None:
    await user_logic.delete_user(db=db, user=current_user)
