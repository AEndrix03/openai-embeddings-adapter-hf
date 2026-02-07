from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapter.middleware.auth import AuthMiddleware
from adapter.settings import Settings


def build_app(settings: Settings) -> TestClient:
    app = FastAPI()
    app.add_middleware(AuthMiddleware, settings=settings)

    @app.get("/ok")
    def ok() -> dict[str, bool]:
        return {"ok": True}

    return TestClient(app)


def test_auth_none() -> None:
    client = build_app(Settings(auth_mode="none"))
    assert client.get("/ok").status_code == 200


def test_auth_bearer_fail() -> None:
    client = build_app(Settings(auth_mode="bearer", auth_bearer_token="t"))
    assert client.get("/ok").status_code == 401


def test_auth_bearer_ok() -> None:
    client = build_app(Settings(auth_mode="bearer", auth_bearer_token="t"))
    assert client.get("/ok", headers={"Authorization": "Bearer t"}).status_code == 200
