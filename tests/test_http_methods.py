from fastapi.testclient import TestClient

from adapter.main import app


def test_embeddings_accepts_options_head_trace() -> None:
    client = TestClient(app)
    assert client.options("/v1/embeddings").status_code == 204
    assert client.head("/v1/embeddings").status_code == 204
    assert client.request("TRACE", "/v1/embeddings").status_code == 204


def test_info_and_health_accept_options_trace() -> None:
    client = TestClient(app)
    assert client.options("/info").status_code == 204
    assert client.request("TRACE", "/livez").status_code == 204
