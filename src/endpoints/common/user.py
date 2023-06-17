from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jose import jwt

from settings.config import get_config, auth_config
from settings.database import get_db
from src.schemas.common.user import UserCreate, Token
from src.schemas.common.common import CreateSuccess
from src.crud.common.user import *

router = APIRouter(
    prefix='/api/user',
)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CreateSuccess)
async def user_create(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_existing_user(db, user_create)

    conflict_email = [u for u in existing_user if user_create.email == u.email]
    conflict_username = [u for u in existing_user if user_create.username == u.username]
    if conflict_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email conflict'
        )
    elif conflict_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username conflict'
        )

    await create_user(db, user_create)
    return CreateSuccess()


@router.post('/login', response_model=Token)
async def user_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):

    # check user and password
    user = await get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # create access token
    data = {
        'sub': user.username,
        'exp': datetime.utcnow() +
            timedelta(minutes=int(get_config()['AUTH'].get('token_expire_minutes')))
    }
    access_token = jwt.encode(
        claims=data,
        key=auth_config.secret_key,
        algorithm=auth_config.algorithm
    )

    return Token(access_token=access_token, token_type='bearer', username=user.username)  # type: ignore