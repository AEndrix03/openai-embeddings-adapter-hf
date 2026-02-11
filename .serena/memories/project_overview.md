# Project overview
- Purpose: FastAPI service exposing an OpenAI-compatible `POST /v1/embeddings` endpoint backed by a single Hugging Face model per container.
- Stack: Python 3.11+, FastAPI, Pydantic Settings, Transformers, PyTorch, Prometheus, OpenTelemetry.
- Packaging/layout: `src/adapter` package, tests in `tests/`, docs in `docs/`, deployment assets in `docker-compose.yml`, Dockerfiles, and `k8s/` overlays.
- Runtime variants: CPU and GPU deployment paths are provided.