from __future__ import annotations

import time

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

HTTP_REQUESTS_TOTAL = Counter(
    "adapter_http_requests_total", "HTTP requests", ["method", "route", "status"]
)
HTTP_REQUEST_LATENCY_SECONDS = Histogram(
    "adapter_http_request_latency_seconds", "HTTP request latency", ["route"]
)
EMBED_REQUESTS_TOTAL = Counter("adapter_embed_requests_total", "Embedding requests total")
EMBED_DURATION_SECONDS = Histogram("adapter_embed_duration_seconds", "Embedding duration seconds")
MODEL_LOADED = Gauge("adapter_model_loaded", "Model loaded state")
DRAIN_MODE = Gauge("adapter_drain_mode", "Drain mode state")


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        start = time.perf_counter()
        response = await call_next(request)
        route = request.url.path
        status = str(response.status_code)
        HTTP_REQUESTS_TOTAL.labels(request.method, route, status).inc()
        HTTP_REQUEST_LATENCY_SECONDS.labels(route).observe(time.perf_counter() - start)
        return response


def metrics_router() -> APIRouter:
    router = APIRouter()

    @router.get("/metrics")
    def metrics() -> PlainTextResponse:
        return PlainTextResponse(generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)

    return router
