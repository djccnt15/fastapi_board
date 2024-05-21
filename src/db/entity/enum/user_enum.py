from enum import IntEnum


class UserEntityEnum(IntEnum):
    NAME = 100
    EMAIL = 255
    PASSWORDMAX = 255
    PASSWORDMIN = 8


class RoleEntityEnum(IntEnum):
    NAME = 50


class StateEntityEnum(IntEnum):
    NAME = 50


class UserStateEntityEnum(IntEnum):
    DETAIL = 500
