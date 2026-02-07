from __future__ import annotations

import torch
import torch.nn.functional as F

from adapter.hints_cpm import CpmHints
from adapter.model_loader import LoadedModel
from adapter.utils.errors import openai_http_exception


def mean_pooling(last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
    summed = torch.sum(last_hidden_state * mask, dim=1)
    counts = torch.clamp(mask.sum(dim=1), min=1e-9)
    return summed / counts


def enforce_dimensions(
    vectors: torch.Tensor,
    model_dim: int,
    body_dimensions: int | None,
    hints: CpmHints,
) -> torch.Tensor:
    requested_dim = body_dimensions or hints.embedding_dim
    if requested_dim is None:
        return vectors
    if requested_dim > model_dim:
        raise openai_http_exception(400, "requested dimensions exceed model output", "dimensions")
    return vectors[:, :requested_dim]


def create_embeddings(
    loaded: LoadedModel,
    inputs: list[str],
    normalize: bool,
    body_dimensions: int | None,
    hints: CpmHints,
    max_length: int,
) -> list[list[float]]:
    encoded = loaded.tokenizer(
        inputs,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    encoded = {k: v.to(loaded.model.device) for k, v in encoded.items()}
    with torch.no_grad():
        out = loaded.model(**encoded)
    pooled = mean_pooling(out.last_hidden_state, encoded["attention_mask"])
    if normalize:
        pooled = F.normalize(pooled, p=2, dim=1)
    pooled = enforce_dimensions(pooled, loaded.embedding_dim, body_dimensions, hints)
    return pooled.cpu().tolist()
