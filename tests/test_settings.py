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
