from fastapi import APIRouter

from src.endpoints.board_qna.question import router as router_question

router = APIRouter()

router.include_router(router_question)