from uuid import uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Log


async def create_log(db: AsyncSession, date_create: datetime, log: str):
    q = Log(
        id=uuid4(),
        date_create=date_create,
        log=log
    )
    db.add(q)
    await db.commit()
    await db.close()