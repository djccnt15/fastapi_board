from enum import StrEnum, auto


class UserRoleEnum(StrEnum): ...


class UserStateEnum(StrEnum):
    BLOCKED = auto()
    INACTIVATE = auto()
