from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from settings.config import get_config, mode
from settings.routes import router
from settings.database import engine
from src.crud.common.log import create_log

app = FastAPI()

origins = get_config()['CORSLIST'].get(mode).split()  # get CORS allow list

app.add_middleware(  # allow CORS credential
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Routers
app.include_router(router)


@app.middleware('http')
async def logger(request: Request, call_next):
    log = {
        'req_url': str(request.url),
        'req_method': str(request.method),
        'param_query': str(dict(request.query_params)),
        'param_path': str(request.path_params),
        'client': str(request.client)
    }
    await create_log(AsyncSession(bind=engine), datetime.now(), str(log))
    response = await call_next(request)
    return response


@app.get('/robots.txt', response_class=PlainTextResponse)
def robots():
    data = 'User-agent: *\nAllow: /'
    return data


@app.get('/', response_class=RedirectResponse)  # temporal index page redirect to swagger
async def root():
    return '/docs'