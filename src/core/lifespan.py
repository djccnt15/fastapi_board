from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.caching.command import redis_cmd
from src.db import database
from src.db.query import db_read


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Check DB/Redis availability
    await db_read.ping()
    await redis_cmd.ping()

    yield

    # close DB engine
    await database.engine.dispose()
