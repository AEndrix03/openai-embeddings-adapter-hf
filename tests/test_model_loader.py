import torch
import pytest

from adapter.model_loader import ModelLoader
from adapter.settings import Settings

def test_resolve_device_maps_rocm_to_cuda(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    loader = ModelLoader(Settings(model_device="rocm"))
    assert loader._resolve_device() == "cuda"


def test_auto_dtype_uses_float16_for_rocm_device(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    loader = ModelLoader(Settings(model_device="rocm", model_dtype="auto"))
    assert loader._resolve_dtype() is torch.float16


def test_resolve_device_rocm_requires_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    loader = ModelLoader(Settings(model_device="rocm"))
    with pytest.raises(RuntimeError, match="ADAPTER_MODEL_DEVICE=rocm requested"):
        loader._resolve_device()


def test_resolve_device_cuda_requires_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    loader = ModelLoader(Settings(model_device="cuda"))
    with pytest.raises(RuntimeError, match="ADAPTER_MODEL_DEVICE=cuda requested"):
        loader._resolve_device()


def test_validate_loading_info_raises_when_strict_enabled() -> None:
    loader = ModelLoader(Settings(model_strict_loading=True))
    with pytest.raises(RuntimeError):
        loader._validate_loading_info({"missing_keys": ["a"], "unexpected_keys": ["b"]})


def test_validate_loading_info_allows_when_strict_disabled() -> None:
    loader = ModelLoader(Settings(model_strict_loading=False))
    loader._validate_loading_info({"missing_keys": ["a"], "unexpected_keys": ["b"]})
