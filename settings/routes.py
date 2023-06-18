from fastapi import APIRouter

from src.endpoints.board.post import router as router_post
from src.endpoints.board.comment import router as router_comment
from src.endpoints.common.user import router as router_user

router = APIRouter()

router.include_router(router_post)
router.include_router(router_comment)
router.include_router(router_user)