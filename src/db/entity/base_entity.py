from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.types import BigInteger


class BaseEntity(DeclarativeBase):
    id = mapped_column(
        type_=BigInteger,
        primary_key=True,
        autoincrement=True,
        sort_order=-1,
    )
