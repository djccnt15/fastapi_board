from fastapi import APIRouter
from starlette.responses import PlainTextResponse, RedirectResponse

router = APIRouter()


@router.get(path="/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /"


@router.get(path="/", response_class=RedirectResponse)
async def index_redirect():  # temporal index page redirect to swagger
    return "/docs"


@router.get(path="/health")
async def helath():
    return 1


@router.get(path="/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"
