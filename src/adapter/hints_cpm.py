from __future__ import annotations

from dataclasses import dataclass

from fastapi import Header


@dataclass
class CpmHints:
    embedding_dim: int | None = None
    normalize: bool | None = None
    task: str | None = None
    model_hint: str | None = None


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError("invalid boolean header")


def parse_cpm_hints(
    x_embedding_dim: str | None = Header(default=None, alias="X-Embedding-Dim"),
    x_embedding_normalize: str | None = Header(default=None, alias="X-Embedding-Normalize"),
    x_embedding_task: str | None = Header(default=None, alias="X-Embedding-Task"),
    x_model_hint: str | None = Header(default=None, alias="X-Model-Hint"),
) -> CpmHints:
    dim = int(x_embedding_dim) if x_embedding_dim else None
    return CpmHints(
        embedding_dim=dim,
        normalize=_parse_bool(x_embedding_normalize),
        task=x_embedding_task,
        model_hint=x_model_hint,
    )


def enforce_model_hint(configured_model_id: str, hints: CpmHints, reject_on_mismatch: bool = True) -> None:
    if not hints.model_hint:
        return
    if hints.model_hint == configured_model_id:
        return
    if reject_on_mismatch:
        raise ValueError(
            f"X-Model-Hint mismatch: requested '{hints.model_hint}', configured '{configured_model_id}'"
        )
