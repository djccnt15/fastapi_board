from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from .exceptions import QueryResultEmptyError


def add_handlers(app: FastAPI) -> None:
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
