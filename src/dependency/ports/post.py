from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Sequence

from src.db.entity.post_entity import PostContentEntity, PostEntity


class PostRepository(ABC):

    @abstractmethod
    async def create_post(
        self,
        *,
        category_id: int,
        created_datetime: datetime,
        user_id: int,
    ) -> int: ...

    @abstractmethod
    async def create_post_detail(
        self,
        *,
        version: int | None = None,
        created_datetime: datetime,
        title: str,
        content: str,
        post_id: int,
    ) -> None: ...

    @abstractmethod
    async def read_post_count(
        self,
        *,
        category_id: int,
        keyword: str,
    ) -> int: ...

    @abstractmethod
    async def read_post_list(
        self,
        *,
        category_id: int,
        keyword: str,
        size: int,
        page: int,
    ) -> Iterable[dict]: ...

    @abstractmethod
    async def read_post(self, *, post_id: int) -> dict: ...

    @abstractmethod
    async def read_post_by_id(self, *, post_id: int) -> PostEntity: ...

    @abstractmethod
    async def read_post_last_version(self, *, post_id: int) -> int: ...

    @abstractmethod
    async def read_post_history(
        self, *, post_id: int
    ) -> Sequence[PostContentEntity]: ...

    @abstractmethod
    async def inactivate_post(self, *, post_id: int) -> None: ...

    @abstractmethod
    async def create_post_vote(
        self,
        *,
        post_id: int,
        user_id: int,
    ) -> None: ...

    @abstractmethod
    async def delete_post_vote(
        self,
        *,
        user_id: int,
        post_id: int,
    ) -> None: ...
