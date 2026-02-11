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
        "max_length_tokens": s.max_length_tokens,
        "model_trust_remote_code": s.model_trust_remote_code,
        "model_strict_loading": s.model_strict_loading,
        "rate_limit_enabled": s.rate_limit_enabled,
        "rate_limit_rps": s.rate_limit_rps,
        "rate_limit_burst": s.rate_limit_burst,
        "metrics_enabled": s.metrics_enabled,
        "otel_enabled": s.otel_enabled,
        "strict_readiness": s.strict_readiness,
    }
