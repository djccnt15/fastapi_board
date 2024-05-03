from fastapi import APIRouter

from ..domain.default.endpoint import default_controller
from .enums import tag

router = APIRouter()

router.include_router(
    router=default_controller.router,
    tags=[tag.RouterTagEnum.DEFAULT],
)
