import logging

from fastapi import Request, Response
from logstash_async.formatter import LogstashFormatter
from logstash_async.handler import AsynchronousLogstashHandler
from starlette.middleware.base import BaseHTTPMiddleware

from src.core import configs

# Logstash handler
logstash_handler = AsynchronousLogstashHandler(**configs.config.logstash)
logstash_handler.setFormatter(LogstashFormatter())

# base logger
logger = logging.getLogger("fastapi")
logger.setLevel(logging.DEBUG)
logger.addHandler(logstash_handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # process the request
        response = await call_next(request)

        # logging
        request_log = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client": request.client.host,
        }
        response_log = {
            "status": response.status_code,
            "headers": dict(response.headers),
        }
        log_content = {
            "request": request_log,
            "response": response_log,
        }
        logger.info(f"LOG: {log_content}")

        return response
