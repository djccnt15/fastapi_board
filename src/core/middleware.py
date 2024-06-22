import time

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.core import configs, log, metrics

config = configs.config.fastapi


def add_middleware(*, app: FastAPI):
    app.add_middleware(  # allow CORS credential
        middleware_class=CORSMiddleware,
        allow_origins=config.cors_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # request logger
    app.add_middleware(middleware_class=log.LoggingMiddleware)
    app.add_middleware(middleware_class=log.RequestBodyLoggingMiddleware)

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        request_latency = time.time() - start_time

        # Increment counters and histograms
        metrics.REQUEST_COUNT.labels(
            "fastapi_app", request.method, request.url.path, response.status_code
        ).inc()
        metrics.REQUEST_LATENCY.labels("fastapi_app", request.url.path).observe(
            amount=request_latency
        )

        return response
