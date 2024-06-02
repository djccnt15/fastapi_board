from typing import Iterable

from pydantic import BaseModel, ConfigDict

from src.domain.post.model import post_response


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class PostListResponse(BaseModel):
    total: int
    post_list: Iterable[post_response.BoardPostResponse]
