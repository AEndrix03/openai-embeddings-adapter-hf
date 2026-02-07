from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from adapter.embedding_engine import create_embeddings
from adapter.hints_cpm import CpmHints, enforce_model_hint, parse_cpm_hints
from adapter.schemas_openai import (
    EmbeddingsRequest,
    EmbeddingsResponse,
    normalize_input,
    to_openai_response,
)
from adapter.settings import get_settings
from adapter.utils.response_cache import build_cache_key
from adapter.utils.text_limits import validate_text_limits

router = APIRouter(tags=["embeddings"])


@router.post("/v1/embeddings", response_model=EmbeddingsResponse)
def create_embeddings_route(
    body: EmbeddingsRequest,
    request: Request,
    hints: Annotated[CpmHints, Depends(parse_cpm_hints)],
) -> EmbeddingsResponse:
    settings = get_settings()
    enforce_model_hint(settings.model_id, hints, reject_on_mismatch=True)

    items = normalize_input(body.input)
    validate_text_limits(
        items,
        max_batch_size=settings.max_batch_size,
        max_chars_per_item=settings.max_chars_per_item,
        max_total_chars=settings.max_total_chars,
    )

    loaded = request.app.state.model_loader.get_or_load()
    normalize = hints.normalize if hints.normalize is not None else settings.default_normalize
    cache = getattr(request.app.state, "embedding_cache", None)
    cache_key = None
    if settings.cache_enabled and cache is not None:
        cache_key = build_cache_key(
            model_id=settings.model_id,
            inputs=items,
            normalize=normalize,
            dimensions=body.dimensions or hints.embedding_dim,
            task=hints.task,
        )
        cached_vectors = cache.get(cache_key)
        if cached_vectors is not None:
            cached_response = to_openai_response(settings.model_id, cached_vectors)
            cached_response.data = sorted(cached_response.data, key=lambda x: x.index)
            cached_response.usage.prompt_tokens = 0
            cached_response.usage.total_tokens = 0
            return cached_response

    vectors = create_embeddings(
        loaded,
        inputs=items,
        normalize=normalize,
        body_dimensions=body.dimensions,
        hints=hints,
        max_length=settings.max_length_tokens,
    )
    if cache_key is not None and settings.cache_enabled and cache is not None:
        cache.set(cache_key, vectors)

    response = to_openai_response(settings.model_id, vectors)
    response.data = sorted(response.data, key=lambda x: x.index)
    response.usage.prompt_tokens = 0
    response.usage.total_tokens = 0
    return response
