from enum import StrEnum


class CacheKeyEnum(StrEnum):
    USER_KEY = "user:%s"
    POST_KEY = "post:%s"
