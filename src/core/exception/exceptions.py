class QueryResultEmptyError(Exception): ...


class WhiteSpaceError(Exception):
    def __init__(self, *args: object, field: str | None) -> None:
        super().__init__(*args)
        self.field = field


class NotUniqueError(Exception):
    def __init__(self, *args: object, field: str) -> None:
        super().__init__(*args)
        self.field = field


class InvalidUserError(Exception): ...
