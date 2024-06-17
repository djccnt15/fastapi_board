from fastapi import APIRouter

from src.domain.board.endpoint import board_controller
from src.domain.comment.endpoint import comment_controller
from src.domain.post.endpoint import post_controller
from src.domain.predict.endpoint import predict_controller
from src.domain.user.endpoint import user_controller

from .enums.tag import RouterTagEnum

router = APIRouter(prefix="/v1")

router.include_router(
    router=user_controller.router,
    tags=[RouterTagEnum.USER],
)

router.include_router(
    router=board_controller.router,
    tags=[RouterTagEnum.BOARD],
)

router.include_router(
    router=post_controller.router,
    tags=[RouterTagEnum.POST],
)

router.include_router(
    router=comment_controller.router,
    tags=[RouterTagEnum.COMMENT],
)

router.include_router(
    router=predict_controller.router,
    tags=[RouterTagEnum.PREDICT],
)
