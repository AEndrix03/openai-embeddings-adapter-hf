from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from adapter.settings import Settings
from adapter.utils.errors import openai_error_dict


@dataclass
class Bucket:
    tokens: float
    updated_at: float


class TokenBucketLimiter:
    def __init__(self, rps: float, burst: int):
        self.rps = rps
        self.burst = float(burst)
        self.buckets: dict[str, Bucket] = {}
        self.lock = threading.Lock()

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        with self.lock:
            bucket = self.buckets.get(key)
            if bucket is None:
                self.buckets[key] = Bucket(tokens=self.burst - 1, updated_at=now)
                return True
            elapsed = now - bucket.updated_at
            bucket.tokens = min(self.burst, bucket.tokens + elapsed * self.rps)
            bucket.updated_at = now
            if bucket.tokens >= 1:
                bucket.tokens -= 1
                return True
            return False


def request_key(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth
    client = request.client.host if request.client else "unknown"
    return f"ip:{client}"


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings):  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.settings = settings
        self.limiter = TokenBucketLimiter(settings.rate_limit_rps, settings.rate_limit_burst)

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if not self.settings.rate_limit_enabled:
            return await call_next(request)
        if not self.limiter.allow(request_key(request)):
            return JSONResponse(status_code=429, content=openai_error_dict(429, "rate limit exceeded"))
        return await call_next(request)
