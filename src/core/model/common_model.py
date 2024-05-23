from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

ID = TypeVar("ID", int, UUID)


class IdModel(BaseModel, Generic[ID]):
    model_config = ConfigDict(validate_assignment=True)

    id: ID


class IdList(BaseModel, Generic[ID]):
    model_config = ConfigDict(validate_assignment=True)

    id_list: list[ID]
