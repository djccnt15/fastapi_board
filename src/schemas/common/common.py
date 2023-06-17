from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel

ID = TypeVar("ID", int, UUID)


class Id(GenericModel, Generic[ID]):
    id: ID


class IdList(GenericModel, Generic[ID]):
    id_list: list[ID]


class CreateSuccess(BaseModel):
    detail: str = 'create success'