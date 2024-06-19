from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    name="request_count",
    documentation="App Request Count",
    labelnames=["app_name", "method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    name="request_latency_seconds",
    documentation="Request latency",
    labelnames=["app_name", "endpoint"],
)
