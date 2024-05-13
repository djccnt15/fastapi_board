class QueryResultEmptyError(Exception): ...


class AlphanumericError(Exception):
    def __init__(self, *args: object, field: str | None) -> None:
        super().__init__(*args)
        self.field = field


class WhiteSpaceError(Exception):
    def __init__(self, *args: object, field: str | None) -> None:
        super().__init__(*args)
        self.field = field


class PasswordNotMatchError(Exception): ...


class NotUniqueError(Exception):
    def __init__(self, *args: object, field: str) -> None:
        super().__init__(*args)
        self.field = field
