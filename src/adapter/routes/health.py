from __future__ import annotations

from fastapi import APIRouter, Request

from adapter.settings import get_settings

router = APIRouter(tags=["health"])


@router.get("/livez")
def livez() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/readyz")
def readyz(request: Request) -> tuple[dict[str, str], int] | dict[str, str]:
    settings = get_settings()
    if getattr(request.app.state, "drain_mode", False):
        return {"status": "not_ready", "reason": "drain_mode"}
    if settings.strict_readiness and not getattr(request.app.state, "model_loaded", False):
        return {"status": "not_ready", "reason": "model_not_loaded"}
    return {"status": "ready"}


@router.get("/healthz")
def healthz(request: Request) -> dict[str, object]:
    return {
        "status": "ok",
        "drain_mode": getattr(request.app.state, "drain_mode", False),
        "model_loaded": getattr(request.app.state, "model_loaded", False),
    }
