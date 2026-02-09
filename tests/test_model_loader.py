import torch

from adapter.model_loader import ModelLoader
from adapter.settings import Settings


def test_resolve_device_maps_rocm_to_cuda() -> None:
    loader = ModelLoader(Settings(model_device="rocm"))
    assert loader._resolve_device() == "cuda"


def test_auto_dtype_uses_float16_for_rocm_device() -> None:
    loader = ModelLoader(Settings(model_device="rocm", model_dtype="auto"))
    assert loader._resolve_dtype() is torch.float16
