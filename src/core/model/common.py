from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

ID = TypeVar("ID", int, UUID, str)


class IdModel(BaseModel, Generic[ID]):
    id: ID


class IdList(BaseModel, Generic[ID]):
    id_list: list[ID]
