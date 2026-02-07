from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from adapter.middleware.auth import AuthMiddleware
from adapter.middleware.rate_limit import RateLimitMiddleware
from adapter.model_loader import ModelLoader
from adapter.observability.logging import AccessLogMiddleware, configure_logging
from adapter.observability.metrics import MetricsMiddleware, metrics_router
from adapter.observability.otel import configure_otel
from adapter.observability.request_id import RequestIdMiddleware
from adapter.routes.embeddings import router as embeddings_router
from adapter.routes.health import router as health_router
from adapter.settings import get_settings
from adapter.utils.errors import openai_error_dict

settings = get_settings()
configure_logging(settings.log_json)

app = FastAPI(title="HF OpenAI Embeddings Adapter")
app.state.model_loader = ModelLoader(settings)
app.state.drain_mode = False
app.state.model_loaded = False

app.add_middleware(RequestIdMiddleware)
app.add_middleware(AccessLogMiddleware)
app.add_middleware(AuthMiddleware, settings=settings)
app.add_middleware(RateLimitMiddleware, settings=settings)
app.add_middleware(MetricsMiddleware)

app.include_router(embeddings_router)
app.include_router(health_router)
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
