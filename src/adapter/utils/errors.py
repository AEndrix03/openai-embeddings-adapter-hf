from __future__ import annotations

from typing import Any

from fastapi import HTTPException

STATUS_TO_ERROR = {
    400: ("invalid_request_error", "invalid_input"),
    401: ("authentication_error", "unauthorized"),
    403: ("permission_error", "forbidden"),
    429: ("rate_limit_error", "rate_limited"),
    503: ("server_error", "service_unavailable"),
}


def openai_error_dict(status_code: int, message: str, param: str | None = None) -> dict[str, Any]:
    err_type, code = STATUS_TO_ERROR.get(status_code, ("server_error", "internal_error"))
    return {"error": {"message": message, "type": err_type, "param": param, "code": code}}


def openai_http_exception(
    status_code: int, message: str, param: str | None = None
) -> HTTPException:
    return HTTPException(
        status_code=status_code, detail=openai_error_dict(status_code, message, param)["error"]
    )
