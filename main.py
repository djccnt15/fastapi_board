from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import configs
from src.common.exception import handlers as exception_handler
from src.routes import default

config = configs.config.fastapi

app = FastAPI(**config)

# API Routers
app.include_router(router=default.router)

# Exception Handler
exception_handler.add_handlers(app=app)

app.add_middleware(  # allow CORS credential
    CORSMiddleware,
    allow_origins=config.cors_orign,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn_config = configs.config.uvicorn

    uvicorn.run(
        # app="main:app",  # use this line when reload config is true
        app=app,
        **uvicorn_config
    )
