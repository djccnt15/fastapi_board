from sqlalchemy.sql import select

from ..database import with_db


async def ping():
    q = select(1)

    async with with_db() as db:
        res = await db.execute(q)
    return res.scalar()
