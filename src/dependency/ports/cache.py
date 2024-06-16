from abc import ABC, abstractmethod


class CacheRepository(ABC):

    @abstractmethod
    async def create_map_cache(
        self,
        *,
        key: str,
        time: int = 30,
        data: dict,
    ) -> None: ...

    @abstractmethod
    async def read_map_cache(self, *, key: str) -> dict | None: ...

    @abstractmethod
    async def delete_cache(self, *, key: str) -> None: ...
