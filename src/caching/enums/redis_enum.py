from enum import StrEnum


class RedisKeyEnum(StrEnum):
    USER_KEY = "user:%s"
    POST_KEY = "post:%s"
