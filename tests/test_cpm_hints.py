import pytest

from adapter.hints_cpm import CpmHints, enforce_model_hint


def test_model_hint_match() -> None:
    enforce_model_hint("model-a", CpmHints(model_hint="model-a"), reject_on_mismatch=True)


def test_model_hint_mismatch_rejected() -> None:
    with pytest.raises(ValueError):
        enforce_model_hint("model-a", CpmHints(model_hint="model-b"), reject_on_mismatch=True)
