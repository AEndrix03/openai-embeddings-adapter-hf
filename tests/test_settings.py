import pytest
from pydantic import ValidationError

from adapter.settings import Settings


def test_default_settings() -> None:
    s = Settings()
    assert s.model_id
    assert s.max_batch_size > 0


def test_bearer_requires_token() -> None:
    with pytest.raises(ValidationError):
        Settings(auth_mode="bearer")


def test_basic_requires_credentials() -> None:
    with pytest.raises(ValidationError):
        Settings(auth_mode="basic", auth_basic_username="u")


def test_eager_load_backward_compatibility() -> None:
    s = Settings(eager_load_model=True)
    assert s.load_model_on_startup is True


def test_load_model_on_startup_flag() -> None:
    s = Settings(load_model_on_startup=True)
    assert s.load_model_on_startup is True


def test_cache_settings_validation() -> None:
    s = Settings(cache_enabled=True, cache_path="tmp/cache.sqlite3", cache_max_entries=100)
    assert s.cache_enabled is True
    assert s.cache_max_entries == 100


def test_model_device_accepts_rocm() -> None:
    s = Settings(model_device="rocm")
    assert s.model_device == "rocm"


def test_rate_limit_settings_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ADAPTER_RATE_LIMIT_ENABLED", "false")
    monkeypatch.setenv("ADAPTER_RATE_LIMIT_RPS", "120")
    monkeypatch.setenv("ADAPTER_RATE_LIMIT_BURST", "240")
    s = Settings()
    assert s.rate_limit_enabled is False
    assert s.rate_limit_rps == 120
    assert s.rate_limit_burst == 240


def test_max_length_tokens_must_be_at_least_two() -> None:
    with pytest.raises(ValidationError):
        Settings(max_length_tokens=1)


def test_rate_limit_rps_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        Settings(rate_limit_rps=0)
