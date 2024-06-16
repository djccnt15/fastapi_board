from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Sequence

from src.db.entity.comment_entity import CommentContentEntity, CommentEntity


class CommentRepository(ABC):

    @abstractmethod
    async def create_comment(
        self,
        *,
        user_id: int,
        post_id: int,
        created_datetime: datetime,
    ) -> int: ...

    @abstractmethod
    async def create_comment_detail(
        self,
        *,
        version: int | None = None,
        created_datetime: datetime,
        content: str,
        comment_id: int,
    ) -> None: ...

    @abstractmethod
    async def read_comment_by_id(self, *, comment_id: int) -> CommentEntity: ...

    @abstractmethod
    async def read_comment_by_post_id(
        self, *, post_id: int
    ) -> Sequence[CommentEntity]: ...

    @abstractmethod
    async def read_comment_list(self, *, post_id: int) -> Iterable[dict]: ...

    @abstractmethod
    async def read_comment_last_version(self, *, comment_id: int) -> int: ...

    @abstractmethod
    async def read_comment_history(
        self, *, comment_id: int
    ) -> Sequence[CommentContentEntity]: ...

    @abstractmethod
    async def inactivate_comment(self, *, comment_id: int) -> None: ...

    @abstractmethod
    async def create_comment_vote(
        self,
        *,
        comment_id: int,
        user_id: int,
    ) -> None: ...

    @abstractmethod
    async def delete_comment_vote(
        self,
        *,
        user_id: int,
        comment_id: int,
    ) -> None: ...
