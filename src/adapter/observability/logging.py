from __future__ import annotations

import json
import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from adapter.observability.request_id import get_request_id

logger = logging.getLogger("adapter")


def configure_logging(json_logs: bool = False) -> None:
    logging.basicConfig(level=logging.INFO)
    if json_logs:
        logger.handlers.clear()


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        start = time.perf_counter()
        response = await call_next(request)
        latency_ms = (time.perf_counter() - start) * 1000
        payload = {
            "event": "http_request",
            "request_id": get_request_id(),
            "method": request.method,
            "route": request.url.path,
            "status": response.status_code,
            "latency_ms": round(latency_ms, 2),
        }
        logger.info(json.dumps(payload))
        return response
