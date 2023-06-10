import json

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from addict import Dict

from settings.config import get_config, mode, dir_config

db_key = dir_config / get_config()['DATABASE'].get('db')

with open(file=db_key, mode='r') as f:
    db_key = Dict(json.load(fp=f)).db[mode]

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername=db_key.drivername,
    username=db_key.username if db_key.username else None,
    password=db_key.password if db_key.password else None,
    host=db_key.host if db_key.host else None,
    port=db_key.port if db_key.port else None,
    database=db_key.database,
)

if str(SQLALCHEMY_DATABASE_URL).startswith("sqlite"):  # check_same_thread arg is only for SQLite
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


async def get_db():
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        await db.close()


Base = declarative_base()

if __name__ == '__main__':
    print(SQLALCHEMY_DATABASE_URL)