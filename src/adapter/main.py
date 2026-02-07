from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from adapter.observability.request_id import RequestIdMiddleware
from adapter.settings import get_settings
from adapter.utils.errors import openai_error_dict

app = FastAPI(title="HF OpenAI Embeddings Adapter")
app.add_middleware(RequestIdMiddleware)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "hf-openai-embeddings-adapter"}


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    payload = openai_error_dict(503, f"internal server error: {type(exc).__name__}")
    return JSONResponse(status_code=503, content=payload)


@app.get("/_settings")
def debug_settings() -> dict[str, str | bool | int | float | None]:
    s = get_settings()
    return {
        "model_id": s.model_id,
        "metrics_enabled": s.metrics_enabled,
    }
