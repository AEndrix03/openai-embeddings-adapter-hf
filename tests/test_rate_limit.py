from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapter.middleware.rate_limit import RateLimitMiddleware
from adapter.settings import Settings


def test_rate_limit_blocks_when_burst_exhausted() -> None:
    app = FastAPI()
    app.add_middleware(
        RateLimitMiddleware,
        settings=Settings(rate_limit_enabled=True, rate_limit_rps=0.1, rate_limit_burst=1),
    )

    @app.get("/ok")
    def ok() -> dict[str, bool]:
        return {"ok": True}

    c = TestClient(app)
    assert c.get("/ok").status_code == 200
    assert c.get("/ok").status_code == 429
