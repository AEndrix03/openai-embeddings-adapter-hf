# HF OpenAI Embeddings Adapter

![CI](https://github.com/example/openai-embeddings-adapter-hf/actions/workflows/ci.yml/badge.svg)

OpenAI-compatible adapter exposing `POST /v1/embeddings` backed by one Hugging Face model per container.

## Runtime matrix

- CPU: `Dockerfile.cpu`, compose profile `cpu`, K8s overlay `cpu`
- CUDA: `Dockerfile.gpu`, compose profile `cuda`, K8s overlay `gpu`
  - default base image: `pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime`
  - override with `CUDA_TORCH_BASE_IMAGE=<image>`
- ROCm 6: `Dockerfile.gpu`, compose profile `rocm6`
  - default base image: `rocm/pytorch:rocm6.4_ubuntu24.04_py3.12_pytorch_release_2.4.1`
  - override with `ROCM6_TORCH_BASE_IMAGE=<image>`

## Startup and cache controls

- `ADAPTER_LOAD_MODEL_ON_STARTUP=true` to preload model during container boot
- `ADAPTER_MODEL_DEVICE` accepts `auto`, `cpu`, `cuda`, `rocm` (`rocm` maps to PyTorch `cuda` runtime)
- `ADAPTER_MODEL_TRUST_REMOTE_CODE=true` for models that require custom HF code
- `ADAPTER_MODEL_STRICT_LOADING=true` fails fast on incompatible checkpoints to avoid degenerate embeddings
- Rate limit via env:
  - `ADAPTER_RATE_LIMIT_ENABLED=true|false`
  - `ADAPTER_RATE_LIMIT_RPS=20`
  - `ADAPTER_RATE_LIMIT_BURST=40`
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
docker compose --profile cuda up --build adapter-cuda
docker compose --profile rocm6 up --build adapter-rocm6
# richiede host ROCm con /dev/kfd e /dev/dri
docker compose --profile rocm6-accel up --build adapter-rocm6-accel
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
