from fastapi import APIRouter

from src.domain.default.endpoint import default_controller, monitoring_controller

from .enums.tag import RouterTagEnum

router = APIRouter()

router.include_router(
    router=default_controller.router,
    tags=[RouterTagEnum.DEFAULT],
)

router.include_router(
    router=monitoring_controller.router,
    tags=[RouterTagEnum.DEFAULT],
)
