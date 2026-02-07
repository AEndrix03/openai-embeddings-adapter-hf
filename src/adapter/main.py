from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from adapter.observability.logging import AccessLogMiddleware, configure_logging
from adapter.observability.metrics import MetricsMiddleware, metrics_router
from adapter.observability.otel import configure_otel
from adapter.observability.request_id import RequestIdMiddleware
from adapter.settings import get_settings
from adapter.utils.errors import openai_error_dict

settings = get_settings()
configure_logging(settings.log_json)

app = FastAPI(title="HF OpenAI Embeddings Adapter")
app.add_middleware(RequestIdMiddleware)
app.add_middleware(AccessLogMiddleware)
app.add_middleware(MetricsMiddleware)
if settings.metrics_enabled:
    app.include_router(metrics_router())
if settings.otel_enabled:
    configure_otel(
        app,
        service_name=settings.service_name,
        model_id=settings.model_id,
        device=settings.model_device,
        endpoint=settings.otel_endpoint,
    )


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
