from datetime import datetime
from io import StringIO
from typing import Iterable, Sequence

import pandas as pd

from src.core.configs import KST
from src.db.entity.post_entity import PostContentEntity
from src.dependency import ports

from ..model import post_response


async def get_post(
    *,
    repo: ports.PostRepository,
    post_id: int,
) -> dict:
    post = await repo.read_post(post_id=post_id)
    return post


async def get_post_history(
    *,
    repo: ports.PostRepository,
    post_id: int,
) -> Sequence[PostContentEntity]:
    post_history = await repo.read_post_history(post_id=post_id)
    return post_history


async def create_post_history_data(
    *,
    data: Iterable[post_response.PostContentResponse],
) -> bytes:
    df = pd.DataFrame(data=(v.model_dump() for v in data))

    with StringIO() as io:
        df.to_csv(path_or_buf=io, index=False)
        csv_content = io.getvalue()

    csv_bytes = csv_content.encode("utf-8")
    return csv_bytes


async def get_comment_list(
    *,
    repo: ports.CommentRepository,
    post_id: int,
) -> Iterable[dict]:
    comment_list = await repo.read_comment_list(post_id=post_id)
    return comment_list


async def update_post(
    *,
    repo: ports.PostRepository,
    title: str,
    content: str,
    post_id: int,
) -> None:
    version = await repo.read_post_last_version(post_id=post_id)
    await repo.create_post_detail(
        version=version + 1,
        created_datetime=datetime.now(KST),
        title=title,
        content=content,
        post_id=post_id,
    )


async def delete_post(
    *,
    repo: ports.PostRepository,
    post_id: int,
) -> None:
    await repo.inactivate_post(post_id=post_id)


async def create_comment(
    *,
    repo: ports.CommentRepository,
    user_id: int,
    post_id: int,
    content: str,
) -> None:
    comment_id = await repo.create_comment(
        user_id=user_id,
        post_id=post_id,
        created_datetime=datetime.now(KST),
    )

    await repo.create_comment_detail(
        created_datetime=datetime.now(KST),
        content=content,
        comment_id=comment_id if comment_id else 0,
    )
