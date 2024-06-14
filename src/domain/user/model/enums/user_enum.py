from enum import StrEnum, auto


class UserRoleEnum(StrEnum):
    ADMIN = auto()


class UserStateEnum(StrEnum):
    BLOCKED = auto()
    INACTIVATE = auto()
