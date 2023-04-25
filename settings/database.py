import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL
from addict import Dict

from settings.config import get_config, mode, dir_config

db_key = Path(dir_config, get_config()['DATABASE'].get('db'))
db_thread_check = get_config()['DATABASE_THREAD_CHECK'].get(mode)

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

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": bool(int(db_thread_check))}  # check_thread is False only for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()