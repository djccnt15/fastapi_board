from pydantic import BaseModel


class Id(BaseModel):
    id: int


class IdList(BaseModel):
    list_id: list[int] = []