from redis.asyncio.client import Redis

from src.caching import redis_db


async def create_expire_hset(
    *,
    redis_key: str,
    time: int,
    data: dict,
) -> None:
    async with redis_db.redis_expire(name=redis_key, time=time) as r:
        await r.hset(name=redis_key, mapping=data)  # type: ignore


async def ping():
    r = Redis.from_pool(connection_pool=redis_db.redis_pool)
    res = await r.ping()
    return res
