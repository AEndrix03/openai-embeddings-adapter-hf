from __future__ import annotations

from fastapi import APIRouter

from adapter.settings import get_settings

router = APIRouter(tags=["version"])


@router.get("/version")
def version() -> dict[str, str]:
    s = get_settings()
    return {"git_sha": s.git_sha, "build_time": s.build_time}
