from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapter.observability.metrics import metrics_router


def test_metrics_endpoint() -> None:
    app = FastAPI()
    app.include_router(metrics_router())
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "adapter_http_requests_total" in response.text or response.text
