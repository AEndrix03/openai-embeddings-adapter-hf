from __future__ import annotations

from fastapi import APIRouter

from adapter.settings import get_settings

router = APIRouter(tags=["info"])


@router.get("/info")
def info() -> dict[str, object]:
    s = get_settings()
    return {
        "service": s.service_name,
        "model_id": s.model_id,
        "device": s.model_device,
        "metrics_enabled": s.metrics_enabled,
        "otel_enabled": s.otel_enabled,
        "strict_readiness": s.strict_readiness,
    }
