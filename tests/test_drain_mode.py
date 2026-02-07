from fastapi.testclient import TestClient

from adapter.main import app


def test_readyz_false_in_drain() -> None:
    client = TestClient(app)
    app.state.drain_mode = True
    resp = client.get("/readyz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "not_ready"
    app.state.drain_mode = False
