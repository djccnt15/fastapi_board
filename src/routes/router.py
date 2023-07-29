from fastapi import APIRouter

from src.endpoints import *
from src.schemas import Tags

router = APIRouter()

router.include_router(
    con_user.router,
    prefix='/user',
    tags=[Tags.auth]
)

router.include_router(
    con_post.router,
    prefix='/board',
    tags=[Tags.board]
)

router.include_router(
    con_comment.router,
    prefix='/board/comment',
    tags=[Tags.board]
)