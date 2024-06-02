from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from .exceptions import (
    InvalidUserError,
    NotUniqueError,
    QueryResultEmptyError,
    WhiteSpaceError,
)


def add_handlers(*, app: FastAPI) -> None:
    @app.exception_handler(QueryResultEmptyError)
    async def empty_query_handler(
        request: Request,
        exc: QueryResultEmptyError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "query result is empty",
            },
        )

    @app.exception_handler(WhiteSpaceError)
    async def white_space_handler(
        request: Request,
        exc: WhiteSpaceError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "field": exc.field,
                "detail": "white space is not allowed",
            },
        )

    @app.exception_handler(NotUniqueError)
    async def unique_exception_handler(
        request: Request,
        exc: NotUniqueError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "field": exc.field,
                "detail": "field must be unique",
            },
        )

    @app.exception_handler(InvalidUserError)
    async def invalid_user_handler(
        request: Request,
        exc: InvalidUserError,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": "invalid user",
            },
        )
