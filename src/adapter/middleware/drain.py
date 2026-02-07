from __future__ import annotations

import signal
import threading
import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from adapter.utils.errors import openai_error_dict


class DrainState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.drain_mode = False
        self.inflight = 0

    def enter(self) -> None:
        with self._lock:
            self.inflight += 1

    def exit(self) -> None:
        with self._lock:
            self.inflight = max(0, self.inflight - 1)

    def set_drain(self, value: bool) -> None:
        with self._lock:
            self.drain_mode = value

    def is_drain(self) -> bool:
        with self._lock:
            return self.drain_mode

    def get_inflight(self) -> int:
        with self._lock:
            return self.inflight


class DrainMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, state: DrainState):  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.state = state

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if self.state.is_drain() and request.url.path not in {"/livez", "/readyz", "/healthz"}:
            return JSONResponse(
                status_code=503,
                content=openai_error_dict(503, "server draining, retry later"),
            )
        self.state.enter()
        try:
            return await call_next(request)
        finally:
            self.state.exit()


def install_sigterm_handler(on_signal: Callable[[], None]) -> None:
    def _handler(signum, frame):  # type: ignore[no-untyped-def]
        on_signal()

    signal.signal(signal.SIGTERM, _handler)


def wait_for_inflight_zero(state: DrainState, timeout_seconds: float) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if state.get_inflight() == 0:
            return
        time.sleep(0.05)
