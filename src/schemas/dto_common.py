from typing import Generic, TypeVar
from uuid import UUID
from enum import Enum

from pydantic import BaseModel
from pydantic.generics import GenericModel

no_id = 'no such id'
no_empty_val = 'empty value is not allowed'
not_val_user = 'not validate user'

ID = TypeVar('ID', int, UUID)


class Id(GenericModel, Generic[ID]):
    id: ID


class IdList(GenericModel, Generic[ID]):
    id_list: list[ID]


class Tags(Enum):
    board = 'Board'
    auth = 'Auth'


class SuccessMsg(BaseModel):
    detail: str


class SuccessCreate(SuccessMsg):
    detail: str = 'create success'


class SuccessUpdate(SuccessMsg):
    detail: str = 'update success'


class SuccessDel(SuccessMsg):
    detail: str = 'delete success'