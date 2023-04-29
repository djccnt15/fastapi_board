from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from settings.database import get_db
from src.schemas.board.post import PostList
from src.crud.board.post import *

router = APIRouter(
    prefix="/api/board",
)


@router.get("/list/{category}", response_model=PostList)
def post_list(category, db: Session = Depends(get_db)):
    total, _post_list = get_post_list(db=db, category=category)
    print(_post_list)
    return {
        'total': total,
        'post_list': _post_list
    }