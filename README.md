# HF OpenAI Embeddings Adapter

OpenAI-compatible adapter that exposes `POST /v1/embeddings` backed by a single Hugging Face model per container.

## Highlights

- OpenAI embeddings contract
- CPM hint headers support
- CPU and GPU deployments
- Probes, metrics, tracing, request-id
- Docker, Kubernetes, CI/CD, security workflows

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn adapter.main:app --reload
```

## Environment

See `.env.example` for all tunables.

## Docker Compose

```bash
docker compose --profile cpu up --build
```

## API

- `POST /v1/embeddings`
- `GET /livez`
- `GET /readyz`
- `GET /healthz`
- `GET /info`
- `GET /version`
- `GET /metrics` (optional)

Detailed specs are in `docs/API.md`.
