from contextlib import asynccontextmanager
from datetime import timedelta

from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from src.core import configs

config = configs.config.redis

redis_pool = ConnectionPool(**config)


async def get_redis():
    r = Redis.from_pool(connection_pool=redis_pool)
    try:
        yield r
    finally:
        await r.aclose()


@asynccontextmanager
async def redis_expire(
    *,
    name: str,
    time: int | timedelta = 30,
):
    r = Redis.from_pool(connection_pool=redis_pool)
    try:
        yield r
    finally:
        await r.expire(name=name, time=time)
        await r.aclose()
