from pydantic import ConfigDict

from src.core.model.common import IdModel


class PostRedisModel(IdModel[int]):
    model_config = ConfigDict(from_attributes=True)

    created_datetime: str
    updated_datetime: str
    category: str
    user: str
    title: str
    content: str
