from fastapi import APIRouter

from ..domain.board.endpoint import board_controller
from ..domain.user.endpoint import user_controller
from .enums.tag import RouterTagEnum

router = APIRouter(prefix="/api")

router.include_router(
    user_controller.router,
    tags=[RouterTagEnum.USER],
)

router.include_router(
    board_controller.router,
    tags=[RouterTagEnum.BOARD],
)
