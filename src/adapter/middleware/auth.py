from __future__ import annotations

import base64

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from adapter.settings import Settings
from adapter.utils.errors import openai_error_dict


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: Settings):  # type: ignore[no-untyped-def]
        super().__init__(app)
        self.settings = settings

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        if self.settings.auth_mode == "none":
            return await call_next(request)

        auth = request.headers.get("Authorization", "")

        if self.settings.auth_mode == "bearer":
            expected = f"Bearer {self.settings.auth_bearer_token}"
            if auth != expected:
                return JSONResponse(
                    status_code=401, content=openai_error_dict(401, "invalid bearer token")
                )
            return await call_next(request)

        if self.settings.auth_mode == "basic":
            if not auth.startswith("Basic "):
                return JSONResponse(
                    status_code=401, content=openai_error_dict(401, "basic auth required")
                )
            encoded = auth.split(" ", 1)[1]
            try:
                decoded = base64.b64decode(encoded).decode("utf-8")
            except Exception:
                return JSONResponse(
                    status_code=401, content=openai_error_dict(401, "invalid basic token")
                )
            username, _, password = decoded.partition(":")
            if (
                username != self.settings.auth_basic_username
                or password != self.settings.auth_basic_password
            ):
                return JSONResponse(status_code=403, content=openai_error_dict(403, "forbidden"))

        return await call_next(request)
