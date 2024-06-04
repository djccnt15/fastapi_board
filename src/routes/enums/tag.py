from enum import StrEnum, auto


class RouterTagEnum(StrEnum):
    DEFAULT = auto()
    USER = auto()
    BOARD = auto()
    POST = auto()
    COMMENT = auto()
    PREDICT = auto()
