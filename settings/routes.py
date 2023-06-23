from fastapi import APIRouter

from src.endpoints import *
from src.schemas import Tags

router = APIRouter()

router.include_router(
    con_user.router,
    prefix='/api/user',
    tags=[Tags.auth]
)

router.include_router(
    con_post.router,
    prefix='/api/board',
    tags=[Tags.board]
)

router.include_router(
    con_comment.router,
    prefix='/api/board/comment',
    tags=[Tags.board]
)