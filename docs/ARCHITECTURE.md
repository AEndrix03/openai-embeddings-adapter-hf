# Architecture

## Overview

The service exposes an OpenAI-compatible embeddings API backed by one Hugging Face model per container.

Request flow:

1. Ingress `POST /v1/embeddings`
2. Request ID assignment and access logging
3. Auth and rate-limit middlewares
4. Drain gate (reject new requests during shutdown)
5. CPM header parsing and validation
6. Input limits validation
7. Model load (lazy/eager) and embedding computation
8. Response shaping to OpenAI contract

## Core components

- `settings.py`: central runtime configuration
- `hints_cpm.py`: CPM header parser and policy
- `model_loader.py`: thread-safe HF tokenizer/model lifecycle
- `embedding_engine.py`: tokenize, forward, mean pooling, normalize, dimensions checks
- `middleware/*`: auth, rate limiting, drain
- `observability/*`: request-id, structured logging, metrics, tracing
- `routes/*`: embeddings, probes, info/version

## Shutdown behavior

- SIGTERM enables drain mode
- readiness turns false
- new traffic gets 503 retryable
- in-flight requests complete within timeout
