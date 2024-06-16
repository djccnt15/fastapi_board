from redis.asyncio.client import Redis

from src.dependency.ports.cache import CacheRepository


class RedisCacheRepository(CacheRepository):

    def __init__(self, *, redis: Redis) -> None:
        self.r = redis

    async def create_map_cache(
        self,
        *,
        key: str,
        time: int = 30,
        data: dict,
    ) -> None:
        await self.r.hset(name=key, mapping=data)  # type: ignore
        await self.r.expire(name=key, time=time)

    async def read_map_cache(self, *, key: str) -> dict | None:
        return await self.r.hgetall(name=key)  # type: ignore

    async def delete_cache(self, *, key: str) -> None:
        await self.r.delete(key)
