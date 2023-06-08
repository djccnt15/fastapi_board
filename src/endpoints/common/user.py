from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings.database import get_db
from src.schemas.common.user import *
from src.crud.common.user import *

router = APIRouter(
    prefix="/api/user",
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def user_create(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_existing_user(db, user_create)
    conflict_email = [u for u in existing_user if u.email == user_create.email]
    conflict_username = [u for u in existing_user if u.username == user_create.username]
    if conflict_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email conflict"
        )
    elif conflict_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username conflict"
        )
    await create_user(db, user_create)