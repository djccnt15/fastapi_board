from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    id: UUID
    version: int
    date_create: datetime
    date_upd: datetime
    content: str
    username: str
    is_superuser: bool | None = None
    is_staff: bool | None = None
    is_blocked: bool | None = None
    is_active: bool

    class Config:
        orm_mode = True