from contextlib import asynccontextmanager

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.core import configs

config = configs.config.db

DB_URL = URL.create(**config.url)
engine = create_async_engine(
    url=DB_URL,
    **config.engine,
)


async def get_db():
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        await db.close()


@asynccontextmanager
async def with_db():
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        await db.close()
