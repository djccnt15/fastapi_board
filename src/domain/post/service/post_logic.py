from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import concurrency

from src.core.configs import KST, TEMP_DIR
from src.core.exception import QueryResultEmptyError
from src.core.utils import pd_to_csv
from src.db.entity import PostContentEntity
from src.db.query.comment import comment_create, comment_read
from src.db.query.post import post_read, post_update

from ..model import post_response


async def get_post(
    *,
    db: AsyncSession,
    post_id: int,
) -> dict:
    post = await post_read.read_post(db=db, post_id=post_id)
    return post


async def get_post_history(
    *,
    db: AsyncSession,
    post_id: int,
) -> Sequence[PostContentEntity]:
    post_history = await post_read.read_post_history(db=db, post_id=post_id)
    if not post_history:
        raise QueryResultEmptyError
    return post_history


async def create_post_history_file(
    *,
    data: Iterable[post_response.PostContentResponse],
    post_id: int,
) -> Path:
    now = datetime.now().replace(microsecond=0)
    file_name = f"POST_HISTORY_{post_id}_{now.strftime('%Y%m%d%H%M')}.csv"
    file_path = TEMP_DIR / file_name
    df = pd.DataFrame(data=(v.model_dump() for v in data))
    await concurrency.run_in_threadpool(func=pd_to_csv, path=file_path, data=df)
    return file_path


async def get_comment_list(
    *,
    db: AsyncSession,
    post_id: int,
) -> Iterable[dict]:
    comment_list = await comment_read.read_comment_list(db=db, post_id=post_id)
    return comment_list


async def update_post(
    *,
    db: AsyncSession,
    title: str,
    content: str,
    post_id: int,
) -> None:
    version = await post_read.read_post_last_version(db=db, post_id=post_id)
    if not version:
        version = 0

    await post_create.create_post_detail(
        db=db,
        version=version + 1,
        created_datetime=datetime.now(KST),
        title=title,
        content=content,
        post_id=post_id,
    )


async def delete_post(
    *,
    db: AsyncSession,
    post_id: int,
) -> None:
    await post_update.inactivate_post(db=db, post_id=post_id)


async def create_comment(
    *,
    db: AsyncSession,
    user_id: int,
    post_id: int,
    content: str,
) -> None:
    comment_id = await comment_create.create_comment(
        db=db,
        user_id=user_id,
        post_id=post_id,
        created_datetime=datetime.now(KST),
    )

    await comment_create.create_comment_detail(
        db=db,
        created_datetime=datetime.now(KST),
        content=content,
        comment_id=comment_id if comment_id else 0,
    )
