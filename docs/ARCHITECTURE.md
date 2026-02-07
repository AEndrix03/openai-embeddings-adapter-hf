# Architecture

## Components

- FastAPI ingress exposing OpenAI-compatible endpoints
- CPM hints parser and validation layer
- Thread-safe model loader for Hugging Face model lifecycle
- Embedding engine (tokenize -> forward -> pooling -> normalize)
- Middleware stack (auth, rate limiting, drain)
- Observability stack (request id, logs, metrics, traces)

## Model loading lifecycle

- Optional eager load at startup
- Lazy load on first inference by default
- Single model instance guarded by lock
- Device and dtype resolved from settings
