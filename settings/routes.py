from fastapi import APIRouter

from src.endpoints.board.post import router as router_post
from src.endpoints.board.comment import router as router_comment
from src.endpoints.common.user import router as router_user
from src.schemas import Tags

router = APIRouter()

router.include_router(
    router_user,
    prefix='/api/user',
    tags=[Tags.auth]
)

router.include_router(
    router_post,
    prefix='/api/board',
    tags=[Tags.board]
)

router.include_router(
    router_comment,
    prefix='/api/board/comment',
    tags=[Tags.board]
)