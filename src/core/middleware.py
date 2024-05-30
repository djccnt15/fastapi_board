from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core import configs

config = configs.config.fastapi


def add_middleware(*, app: FastAPI):
    app.add_middleware(  # allow CORS credential
        middleware_class=CORSMiddleware,
        allow_origins=config.cors_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
