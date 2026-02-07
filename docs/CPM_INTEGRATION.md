# CPM Integration Guide

CPM target endpoint:

- `POST {base_url}/v1/embeddings`

## Header mapping

- `X-Embedding-Dim` -> output dimension request
- `X-Embedding-Normalize` -> normalize true/false
- `X-Embedding-Task` -> task hint for telemetry/routing
- `X-Model-Hint` -> expected model id (mismatch rejected by default)

## Example CPM snippet

```yaml
provider: openai-compatible
base_url: http://adapter:8000
path: /v1/embeddings
headers:
  X-Embedding-Normalize: "true"
  X-Embedding-Task: "retrieval"
timeout_seconds: 30
retry:
  max_attempts: 3
  backoff: exponential
```

## Retry policy

- Retry on `503` (draining/unavailable)
- Backoff and retry on `429`
- Do not retry malformed `400`

## Timeout policy

- Keep connect timeout low
- Use request timeout aligned with model latency profile
