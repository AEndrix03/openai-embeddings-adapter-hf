# API Specification

## POST /v1/embeddings

### Request

```json
{
  "input": ["hello world", "ciao mondo"],
  "model": "optional-model-name",
  "dimensions": 384,
  "encoding_format": "float",
  "user": "optional-user"
}
```

### Supported headers

- `X-Embedding-Dim`
- `X-Embedding-Normalize`
- `X-Embedding-Task`
- `X-Model-Hint`
- `X-Request-Id`

### Success response

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [0.12, -0.04]
    }
  ],
  "model": "sentence-transformers/all-MiniLM-L6-v2",
  "usage": {
    "prompt_tokens": 0,
    "total_tokens": 0
  }
}
```

### Error response schema

```json
{
  "error": {
    "message": "human-readable message",
    "type": "invalid_request_error",
    "param": "input",
    "code": "invalid_input"
  }
}
```

### Status codes

- `400`: invalid request / validation failure
- `401`: unauthorized
- `403`: forbidden
- `429`: rate limited
- `503`: service unavailable / draining

## Probes and metadata

- `GET /livez`
- `GET /readyz`
- `GET /healthz`
- `GET /info`
- `GET /version`
- `GET /metrics` (optional)

## Curl examples

```bash
curl -X POST http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "X-Embedding-Normalize: true" \
  -d '{"input":["hello","world"],"dimensions":256}'
```

```bash
curl http://localhost:8000/readyz
```
