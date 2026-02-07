from __future__ import annotations

import threading
from dataclasses import dataclass

import torch
from transformers import AutoModel, AutoTokenizer

from adapter.settings import Settings


@dataclass
class LoadedModel:
    tokenizer: AutoTokenizer
    model: AutoModel
    device: str
    dtype: str
    embedding_dim: int


class ModelLoader:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._lock = threading.Lock()
        self._loaded: LoadedModel | None = None
        if settings.eager_load_model:
            self.get_or_load()

    def _resolve_device(self) -> str:
        if self.settings.model_device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
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

    def get_or_load(self) -> LoadedModel:
        if self._loaded is not None:
            return self._loaded
        with self._lock:
            if self._loaded is not None:
                return self._loaded
            tokenizer = AutoTokenizer.from_pretrained(self.settings.model_id)
            model = AutoModel.from_pretrained(self.settings.model_id)
            device = self._resolve_device()
            dtype = self._resolve_dtype()
            model = model.to(device=device, dtype=dtype)
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
