from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.ai import model
from src.caching import redis_db
from src.caching.command import redis_cmd
from src.db import database
from src.db.query import db_read


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Check DB/Redis availability
    await db_read.ping()
    await redis_cmd.ping()

    # Load the ML model
    model.load_ml_models()

    yield

    # close DB engine
    await database.engine.dispose()
    await redis_db.redis_pool.aclose()

    # Clean up the ML models and release the resources
    model.clear_resource()
