from pydantic import ConfigDict

from src.core.model import IdModel
from src.domain.user.model import user_request


class UserRedisModel(IdModel[int], user_request.UserBase):
    model_config = ConfigDict(from_attributes=True)

    password: str
    created_datetime: str
