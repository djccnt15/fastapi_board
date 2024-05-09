from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from .exceptions import (
    AlphanumericError,
    InternalServerError,
    NotUniqueError,
    PasswordNotMatchError,
    QueryResultEmptyError,
    WhiteSpaceError,
)


def add_handlers(app: FastAPI) -> None:
    @app.exception_handler(InternalServerError)
    async def internel_error_handler(
        request: Request,
        exc: InternalServerError,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "internal server error, contact to admin",
            },
        )

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

    @app.exception_handler(AlphanumericError)
    async def alphanumeric_handler(
        request: Request,
        exc: AlphanumericError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "field": exc.field,
                "detail": "field must be alphanumeric",
            },
        )

    @app.exception_handler(PasswordNotMatchError)
    async def pw_not_match_handler(
        request: Request,
        exc: PasswordNotMatchError,
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "password1 and password2 are not equal",
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
