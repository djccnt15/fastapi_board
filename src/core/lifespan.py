from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.ai import model
from src.dependency import adapters


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Check DB/Redis availability
    await adapters.db_ping()
    await adapters.redis_ping()

    # Load the ML model
    model.load_ml_models()

    yield

    # close DB engine
    await adapters.db_engine.dispose()
    await adapters.redis_pool.aclose()

    # Clean up the ML models and release the resources
    model.clear_resource()
