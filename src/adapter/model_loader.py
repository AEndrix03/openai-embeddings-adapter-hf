from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any

import torch
from transformers import AutoModel, AutoTokenizer

from adapter.settings import Settings


@dataclass
class LoadedModel:
    tokenizer: Any
    model: Any
    device: str
    dtype: str
    embedding_dim: int


class ModelLoader:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._lock = threading.Lock()
        self._loaded: LoadedModel | None = None
        if settings.load_model_on_startup:
            self.get_or_load()

    def _resolve_device(self) -> str:
        if self.settings.model_device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        if self.settings.model_device == "cuda":
            if not torch.cuda.is_available():
                raise RuntimeError(
                    "ADAPTER_MODEL_DEVICE=cuda requested, but no CUDA/ROCm runtime is available. "
                    "Use ADAPTER_MODEL_DEVICE=cpu or auto."
                )
            return "cuda"
        if self.settings.model_device == "rocm":
            # PyTorch uses "cuda" device strings for ROCm/HIP backends.
            if not torch.cuda.is_available():
                raise RuntimeError(
                    "ADAPTER_MODEL_DEVICE=rocm requested, but no ROCm/HIP runtime is available. "
                    "Use rocm6-safe (ADAPTER_MODEL_DEVICE=auto) or expose /dev/kfd and /dev/dri."
                )
            return "cuda"
        return self.settings.model_device

    def _resolve_dtype(self) -> torch.dtype:
        mapping = {
            "float32": torch.float32,
            "float16": torch.float16,
            "bfloat16": torch.bfloat16,
        }
        if self.settings.model_dtype == "auto":
            return torch.float16 if self._resolve_device() == "cuda" else torch.float32
        return mapping[self.settings.model_dtype]

    def _validate_loading_info(self, loading_info: dict[str, Any]) -> None:
        if not self.settings.model_strict_loading:
            return
        missing = loading_info.get("missing_keys") or []
        unexpected = loading_info.get("unexpected_keys") or []
        if not missing and not unexpected:
            return
        raise RuntimeError(
            "model checkpoint appears incompatible with AutoModel. "
            f"missing_keys={len(missing)}, unexpected_keys={len(unexpected)}. "
            "Set ADAPTER_MODEL_TRUST_REMOTE_CODE=true for models requiring custom code, "
            "or use a checkpoint compatible with transformers AutoModel. "
            "To bypass this validation (not recommended), set ADAPTER_MODEL_STRICT_LOADING=false."
        )

    def get_or_load(self) -> LoadedModel:
        if self._loaded is not None:
            return self._loaded
        with self._lock:
            if self._loaded is not None:
                return self._loaded
            tokenizer = AutoTokenizer.from_pretrained(
                self.settings.model_id,
                trust_remote_code=self.settings.model_trust_remote_code,
            )
            model, loading_info = AutoModel.from_pretrained(
                self.settings.model_id,
                trust_remote_code=self.settings.model_trust_remote_code,
                output_loading_info=True,
            )
            self._validate_loading_info(loading_info)
            device = self._resolve_device()
            dtype = self._resolve_dtype()
            model = model.to(device=device, dtype=dtype)
            model.eval()
            embedding_dim = int(getattr(model.config, "hidden_size", 0) or 0)
            if embedding_dim <= 0:
                raise RuntimeError("unable to infer embedding dimension from model config")
            self._loaded = LoadedModel(
                tokenizer=tokenizer,
                model=model,
                device=device,
                dtype=str(dtype),
                embedding_dim=embedding_dim,
            )
            return self._loaded
