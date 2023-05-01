from pydantic import BaseModel


class Category(BaseModel):
    category: str

    class Config:
        orm_mode = True
