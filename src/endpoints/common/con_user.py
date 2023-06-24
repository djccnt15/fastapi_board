from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jose import jwt

from settings.config import get_config, auth_config
from settings.database import get_db
from src.schemas import *
from src.crud import *
from src.app import get_current_user

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=SuccessCreate)
async def user_create(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    '''
    - one email can be use by only one user
    - user name cannot be used if one is occupied
    - PW1 and PW2 mush be same
    '''

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
    return SuccessCreate()


@router.post('/login', response_model=Token)
async def user_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):

    # check user and password
    user = await get_user(db, form_data.username)
    if user is None or not pwd_context.verify(form_data.password, user.password):
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

    return Token(access_token=access_token, token_type='bearer', username=user.username)


@router.put('/update', response_model=SuccessUpdate)
async def user_update(
        user_update: UserCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    existing_user = await get_conflict_user(db, user_update, current_user.id)

    conflict_email = [u for u in existing_user if user_update.email == u.email]
    conflict_username = [u for u in existing_user if user_update.username == u.username]
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

    await update_user(db, user_update, current_user.id)
    return SuccessUpdate()


@router.delete('/delete', response_model=SuccessDel)
async def user_delete(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await del_user(db, current_user.id)
    return SuccessDel()