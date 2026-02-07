from fastapi.testclient import TestClient

from adapter.main import app


def test_info_endpoint() -> None:
    client = TestClient(app)
    r = client.get("/info")
    assert r.status_code == 200
    assert "model_id" in r.json()


def test_version_endpoint() -> None:
    client = TestClient(app)
    r = client.get("/version")
    assert r.status_code == 200
    body = r.json()
    assert "git_sha" in body
    assert "build_time" in body
