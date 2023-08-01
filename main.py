import json
from datetime import datetime

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.requests import Request

from env.config import get_config, mode, dir_config
from env.database import engine
from src.routes import router
from src.crud import create_log

metadata = get_config()['SWAGGER']

with open(dir_config / metadata.get('description')) as f:
    description = f.read()

with open(dir_config / metadata.get('tags_metadata')) as f:
    tags_metadata = json.load(f)['tags']

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
app.include_router(router, prefix='/api')


# @app.middleware('http')
async def logger(request: Request, call_next):
    log = {
        'req_url': str(request.url),
        'req_method': str(request.method),
        'param_query': str(dict(request.query_params)),
        'param_path': str(request.path_params),
        'client': str(request.client)
    }
    await create_log(engine, datetime.now(), str(log))
    return await call_next(request)


@app.get('/robots.txt', response_class=PlainTextResponse)
def robots():
    return 'User-agent: *\nAllow: /'


@app.get('/', response_class=RedirectResponse)  # temporal index page redirect to swagger
async def root():
    return '/docs'