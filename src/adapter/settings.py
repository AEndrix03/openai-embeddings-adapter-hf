from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ADAPTER_", case_sensitive=False)

    # model/runtime
    model_id: str = "sentence-transformers/all-MiniLM-L6-v2"
    model_device: Literal["auto", "cpu", "cuda", "rocm"] = "auto"
    model_dtype: Literal["auto", "float32", "float16", "bfloat16"] = "auto"
    model_trust_remote_code: bool = False
    model_strict_loading: bool = True
    eager_load_model: bool = False
    load_model_on_startup: bool = False

    # API limits
    max_batch_size: int = 128
    max_chars_per_item: int = 10000
    max_total_chars: int = 100000
    max_length_tokens: int = 512
    default_normalize: bool = True

    # cache
    cache_enabled: bool = True
    cache_path: str = ".cache/embeddings_cache.sqlite3"
    cache_max_entries: int = 100000

    # auth
    auth_mode: Literal["none", "bearer", "basic"] = "none"
    auth_bearer_token: str | None = None
    auth_basic_username: str | None = None
    auth_basic_password: str | None = None

    # observability
    log_json: bool = False
    metrics_enabled: bool = True
    otel_enabled: bool = False
    otel_endpoint: str | None = None
    service_name: str = "hf-openai-embeddings-adapter"

    # rate limit
    rate_limit_enabled: bool = True
    rate_limit_rps: float = 20.0
    rate_limit_burst: int = 40

    # shutdown/drain
    strict_readiness: bool = False
    drain_timeout_seconds: float = 20.0

    # metadata
    git_sha: str = "dev"
    build_time: str = "unknown"

    @model_validator(mode="after")
    def validate_auth(self) -> Settings:
        if self.auth_mode == "bearer" and not self.auth_bearer_token:
            raise ValueError("ADAPTER_AUTH_BEARER_TOKEN is required when auth mode is bearer")
        if self.auth_mode == "basic" and (
            not self.auth_basic_username or not self.auth_basic_password
        ):
            raise ValueError(
                "basic auth requires ADAPTER_AUTH_BASIC_USERNAME and ADAPTER_AUTH_BASIC_PASSWORD"
            )
        if self.max_batch_size < 1:
            raise ValueError("max_batch_size must be >= 1")
        if self.max_length_tokens < 2:
            raise ValueError("max_length_tokens must be >= 2")
        if self.rate_limit_rps <= 0:
            raise ValueError("rate_limit_rps must be > 0")
        if self.rate_limit_burst < 1:
            raise ValueError("rate_limit_burst must be >= 1")
        if self.cache_max_entries < 1:
            raise ValueError("cache_max_entries must be >= 1")
        if self.eager_load_model:
            self.load_model_on_startup = True
        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()
