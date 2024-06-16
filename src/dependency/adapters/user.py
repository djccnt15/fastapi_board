from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert, or_, select, update

from src.db.entity.user_entity import LoggedInEntity, RoleEntity, UserEntity
from src.dependency.ports import UserRepository


class RdbUserRepository(UserRepository):
    def __init__(self, *, db: AsyncSession):
        self.db = db

    async def create_user(
        self,
        *,
        name: str,
        password: str,
        email: str,
        created_datetime: datetime,
    ) -> None:
        q = insert(UserEntity).values(
            name=name,
            password=password,
            email=email,
            created_datetime=created_datetime,
        )
        await self.db.execute(statement=q)
        await self.db.commit()

    async def create_login_log(
        self,
        *,
        user_id: int,
        created_datetime: datetime,
    ) -> None:
        q = insert(LoggedInEntity).values(
            user_id=user_id,
            created_datetime=created_datetime,
        )
        await self.db.execute(statement=q)
        await self.db.commit()

    async def read_user_by_name_email(
        self,
        *,
        name: str,
        email: str,
    ) -> Sequence[UserEntity]:
        q = select(UserEntity).where(
            or_(
                UserEntity.name == name,
                UserEntity.email == email,
            )
        )
        res = await self.db.execute(statement=q)
        return res.scalars().all()

    async def read_user_by_name(self, *, name: str) -> UserEntity | None:
        q = select(UserEntity).where(UserEntity.name == name)
        res = await self.db.execute(statement=q)
        return res.scalar()

    async def read_user_role(self, *, user_id: int) -> RoleEntity:
        q = (
            select(RoleEntity)
            .join(
                target=UserEntity,
                onclause=RoleEntity.id == UserEntity.role_id,
            )
            .where(UserEntity.id == user_id)
        )
        res = await self.db.execute(statement=q)
        return res.scalar_one()

    async def update_user(
        self,
        *,
        user_id: int,
        name: str,
        email: str,
    ) -> None:
        q = (
            update(UserEntity)
            .where(UserEntity.id == user_id)
            .values(name=name, email=email)
        )
        await self.db.execute(statement=q)
        await self.db.commit()

    async def update_password(
        self,
        *,
        user_id: int,
        password: str,
    ) -> None:
        q = update(UserEntity).where(UserEntity.id == user_id).values(password=password)
        await self.db.execute(statement=q)
        await self.db.commit()

    async def resign_user(self, *, user_id: int) -> None:
        q = (
            update(UserEntity)
            .where(UserEntity.id == user_id)
            .values(name=None, password=None, email=None)
        )
        await self.db.execute(statement=q)
        await self.db.commit()
