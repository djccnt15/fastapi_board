from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings.database import get_db
from src.schemas.common.user import UserCreate
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