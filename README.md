# HF OpenAI Embeddings Adapter

![CI](https://github.com/example/openai-embeddings-adapter-hf/actions/workflows/ci.yml/badge.svg)

OpenAI-compatible adapter exposing `POST /v1/embeddings` backed by one Hugging Face model per container.

## Runtime matrix

- CPU: `Dockerfile.cpu`, compose profile `cpu`, K8s overlay `cpu`
- GPU: `Dockerfile.gpu`, compose profile `gpu`, K8s overlay `gpu`

## Startup and cache controls

- `ADAPTER_LOAD_MODEL_ON_STARTUP=true` to preload model during container boot
- Persistent response cache (SQLite/WAL) via:
  - `ADAPTER_CACHE_ENABLED=true`
  - `ADAPTER_CACHE_PATH=/var/cache/adapter/embeddings_cache.sqlite3`
  - `ADAPTER_CACHE_MAX_ENTRIES=100000`

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn adapter.main:app --reload
```

## Docker quickstart

```bash
docker compose --profile cpu up --build
```

## Endpoints

- `POST /v1/embeddings`
- `GET /livez`
- `GET /readyz`
- `GET /healthz`
- `GET /metrics` (optional)
- `GET /info`
- `GET /version`

## Docs

- `docs/API.md`
- `docs/ARCHITECTURE.md`
- `docs/RUNBOOK.md`
- `docs/DEPLOYMENT.md`
- `docs/OBSERVABILITY.md`
- `docs/SECURITY.md`
- `docs/PERFORMANCE.md`
- `docs/CPM_INTEGRATION.md`
