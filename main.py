from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from settings.config import get_config, mode, dir_config
from settings.routes import router
from settings.database import engine
from src.crud import create_log

metadata = get_config()['DEFAULT']

with open(dir_config / metadata.get('description')) as f:
    description = f.read()

tags_metadata = [
    {
        'name': 'default',
        'externalDocs': {
            'description': 'External docs',
            'url': f'{metadata.get("url")}',
        },
    },
    {
        'name': 'Auth',
        'description': 'Operations with users, Such as **SignUp**, **LogIn** logics',
    },
    {
        'name': 'Board',
        'description': 'CRUD Post, Comments',
    },
]

app = FastAPI(
    title=metadata.get('title'),
    version=metadata.get('version'),
    contact={
        'name': metadata.get('name'),
        'url': metadata.get('url'),
        'email': metadata.get('email')
    },
    license_info={
        'name': metadata.get('license_name'),
        'url': metadata.get('license_url')
    },
    description=description,
    openapi_tags=tags_metadata
)

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
    return await call_next(request)


@app.get('/robots.txt', response_class=PlainTextResponse)
def robots():
    return 'User-agent: *\nAllow: /'


@app.get('/', response_class=RedirectResponse)  # temporal index page redirect to swagger
async def root():
    return '/docs'