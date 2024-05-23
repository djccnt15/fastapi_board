from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.auth import get_current_user
from src.core.model.enums import ResponseEnum
from src.db.database import get_db

from ..business import user_process
from ..model import user_request, user_response

router = APIRouter(prefix="/user")


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_user(
    request: user_request.UserCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> ResponseEnum:
    """
    - one email can be used by only one user
    - username cannot be used if one is occupied
    - PW1 and PW2 mush be same
    """
    await user_process.create_user(db=db, request=request)
    return ResponseEnum.CREATE


@router.post(path="/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> user_response.Token:
    token = await user_process.login_user(form_data=form_data, db=db)
    return token


@router.put(path="")
async def update_user(
    request: user_request.UserBase,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await user_process.update_user(
        db=db,
        request=request,
        current_user=current_user,
    )
    return ResponseEnum.UPDATE


@router.put(path="/password")
async def update_password(
    request: user_request.Password,
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await user_process.update_password(
        db=db,
        current_user=current_user,
        data=request,
    )
    return ResponseEnum.UPDATE


@router.delete(path="")
async def resign_user(
    db: AsyncSession = Depends(get_db),
    current_user: user_request.UserCurrent = Depends(get_current_user),
) -> ResponseEnum:
    await user_process.resign_user(db=db, current_user=current_user)
    return ResponseEnum.DELETE
