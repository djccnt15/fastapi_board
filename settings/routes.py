from fastapi import APIRouter

from src.endpoints.board.post import router as router_post

router = APIRouter()

router.include_router(router_post)