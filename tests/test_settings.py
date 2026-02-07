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
