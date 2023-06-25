from fastapi import APIRouter

from src.endpoints import *
from src.schemas import Tags

router = APIRouter()
api = '/api'

router.include_router(
    con_user.router,
    prefix=f'{api}/user',
    tags=[Tags.auth]
)

router.include_router(
    con_post.router,
    prefix=f'{api}/board',
    tags=[Tags.board]
)

router.include_router(
    con_comment.router,
    prefix=f'{api}/board/comment',
    tags=[Tags.board]
)