from typing import Annotated

from fastapi import Depends, Query
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.sql import select

from src.ai import model
from src.core import configs
from src.domain.predict.model.enums.predict_enum import AlgorithmEnum

from .cache import RedisCacheRepository
from .category import RdbCategoryRepository
from .comment import RdbCommentRepository
from .post import RdbPostRepository
from .predict import IrisInferencer
from .user import RdbUserRepository

config = configs.config

DB_URL = URL.create(**config.db.url)
db_engine = create_async_engine(
    url=DB_URL,
    **config.db.engine,
)


async def db_ping():
    db = AsyncSession(bind=db_engine)
    q = select(1)
    try:
        res = await db.execute(statement=q)
    finally:
        await db.close()
    return res.scalar()


async def get_db():
    db = AsyncSession(bind=db_engine)
    try:
        yield db
    finally:
        await db.close()


RepoSession = Annotated[AsyncSession, Depends(get_db)]


async def get_user_repo(db: RepoSession) -> RdbUserRepository:
    return RdbUserRepository(db=db)


async def get_category_repo(db: RepoSession) -> RdbCategoryRepository:
    return RdbCategoryRepository(db=db)


async def get_post_repo(db: RepoSession) -> RdbPostRepository:
    return RdbPostRepository(db=db)


async def get_comment_repo(db: RepoSession) -> RdbCommentRepository:
    return RdbCommentRepository(db=db)


redis_pool = ConnectionPool(**config.redis)


async def redis_ping():
    r = Redis.from_pool(connection_pool=redis_pool)
    res = await r.ping()
    return res


async def get_cache():
    r = Redis.from_pool(connection_pool=redis_pool)
    try:
        yield r
    finally:
        await r.aclose()


async def get_cache_repo(
    cache: Annotated[Redis, Depends(get_cache)]
) -> RedisCacheRepository:
    return RedisCacheRepository(redis=cache)


async def get_iris_inferencer(algorithm: Annotated[AlgorithmEnum, Query()]):
    ai_model = model.iris_classifier.get(algorithm)
    if not ai_model:
        raise ValueError
    return IrisInferencer(model=ai_model)
