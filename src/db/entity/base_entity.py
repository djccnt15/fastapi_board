from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.types import BigInteger


class BaseEntity(DeclarativeBase): ...


class BigintIdEntity(BaseEntity):
    __abstract__ = True

    id = mapped_column(
        type_=BigInteger,
        primary_key=True,
        autoincrement=True,
        sort_order=-1,
    )
