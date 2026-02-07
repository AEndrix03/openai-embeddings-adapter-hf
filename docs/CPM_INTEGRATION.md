# CPM Integration

CPM calls the adapter at `POST /v1/embeddings`.

## Supported hint headers

- `X-Embedding-Dim`: target embedding dimension override
- `X-Embedding-Normalize`: `true/false`
- `X-Embedding-Task`: task string for downstream routing/telemetry
- `X-Model-Hint`: expected model id

## Model hint policy

Default policy rejects model mismatch with HTTP 400.

## Retry guidance

- Retry on `503` (drain/unavailable)
- Backoff on `429`
- Do not retry malformed `400` requests
