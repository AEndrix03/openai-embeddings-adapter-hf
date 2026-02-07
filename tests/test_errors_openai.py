import pytest
from fastapi import HTTPException

from adapter.utils.text_limits import validate_text_limits


def test_limits_ok() -> None:
    validate_text_limits(["a", "bb"], max_batch_size=10, max_chars_per_item=10, max_total_chars=10)


def test_too_many_items() -> None:
    with pytest.raises(HTTPException):
        validate_text_limits(
            ["a", "b", "c"], max_batch_size=2, max_chars_per_item=10, max_total_chars=10
        )


def test_too_many_chars_per_item() -> None:
    with pytest.raises(HTTPException):
        validate_text_limits(["abcdef"], max_batch_size=2, max_chars_per_item=3, max_total_chars=10)


def test_too_many_total_chars() -> None:
    with pytest.raises(HTTPException):
        validate_text_limits(
            ["abcd", "efgh"], max_batch_size=3, max_chars_per_item=10, max_total_chars=7
        )
