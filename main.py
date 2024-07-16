from fastapi import FastAPI

from src.core import configs, exception, lifespan, middleware
from src.routes import api, default

config = configs.config.fastapi

app = FastAPI(**config, lifespan=lifespan.lifespan)

# API Routers
app.include_router(router=default.router)
app.include_router(router=api.router, prefix="/api")

# Exception Handler
exception.add_handlers(app=app)

# add middleware
middleware.add_middleware(app=app)

if __name__ == "__main__":
    import uvicorn

    uvicorn_config = configs.config.uvicorn

    uvicorn.run(app=app, **uvicorn_config)
