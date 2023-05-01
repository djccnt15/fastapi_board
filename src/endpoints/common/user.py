from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from settings.database import get_db
from src.schemas.common.user import *
from src.crud.common.user import *

router = APIRouter(
    prefix="/api/user",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_create: UserCreate, db: Session = Depends(get_db)):
    if get_existing_useremail(db, user_create):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already Signed up"
        )
    elif get_existing_username(db, user_create):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already occupied"
        )
    create_user(db, user_create)