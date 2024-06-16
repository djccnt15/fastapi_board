from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from src.db.entity.user_entity import RoleEntity, UserEntity


class UserRepository(ABC):

    @abstractmethod
    async def create_user(
        self,
        *,
        name: str,
        password: str,
        email: str,
        created_datetime: datetime,
    ) -> None: ...

    @abstractmethod
    async def create_login_log(
        self,
        *,
        user_id: int,
        created_datetime: datetime,
    ) -> None: ...

    @abstractmethod
    async def read_user_by_name_email(
        self,
        *,
        name: str,
        email: str,
    ) -> Sequence[UserEntity]: ...

    @abstractmethod
    async def read_user_by_name(self, *, name: str) -> UserEntity | None: ...

    @abstractmethod
    async def read_user_role(self, *, user_id: int) -> RoleEntity: ...

    @abstractmethod
    async def update_user(
        self,
        *,
        user_id: int,
        name: str,
        email: str,
    ) -> None: ...

    @abstractmethod
    async def update_password(
        self,
        *,
        user_id: int,
        password: str,
    ) -> None: ...

    @abstractmethod
    async def resign_user(self, *, user_id: int) -> None: ...
