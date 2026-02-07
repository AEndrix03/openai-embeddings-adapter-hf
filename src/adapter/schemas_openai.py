from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EmbeddingsRequest(BaseModel):
    input: str | list[str]
    model: str | None = None
    encoding_format: str | None = None
    dimensions: int | None = Field(default=None, ge=1)
    user: str | None = None


class EmbeddingItem(BaseModel):
    object: str = "embedding"
    index: int
    embedding: list[float]


class Usage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingsResponse(BaseModel):
    object: str = "list"
    data: list[EmbeddingItem]
    model: str
    usage: Usage = Field(default_factory=Usage)


class OpenAIErrorBody(BaseModel):
    message: str
    type: str
    param: str | None = None
    code: str | None = None


class OpenAIErrorResponse(BaseModel):
    error: OpenAIErrorBody


def normalize_input(input_value: str | list[str]) -> list[str]:
    if isinstance(input_value, str):
        return [input_value]
    return input_value


def to_openai_response(model: str, vectors: list[list[float]]) -> EmbeddingsResponse:
    items = [EmbeddingItem(index=i, embedding=v) for i, v in enumerate(vectors)]
    return EmbeddingsResponse(model=model, data=items)


def error_payload(message: str, err_type: str, param: str | None = None, code: str | None = None) -> dict[str, Any]:
    return {"error": {"message": message, "type": err_type, "param": param, "code": code}}
