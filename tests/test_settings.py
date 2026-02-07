from adapter.settings import Settings


def test_default_settings() -> None:
    s = Settings()
    assert s.model_id
    assert s.max_batch_size > 0


def test_bearer_requires_token() -> None:
    try:
        Settings(auth_mode="bearer")
        assert False, "expected error"
    except Exception:
        pass


def test_basic_requires_credentials() -> None:
    try:
        Settings(auth_mode="basic", auth_basic_username="u")
        assert False, "expected error"
    except Exception:
        pass
