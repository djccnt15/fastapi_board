from enum import StrEnum, auto


class BoardEnum(StrEnum):
    QNA = auto()
    COMMUNITY = auto()


class CategoryEnum(StrEnum):
    CAREER = auto()
    TECH = auto()
    LIFE = auto()
    NEWS = auto()
