# API Contract

## POST /v1/embeddings

OpenAI-compatible endpoint for embeddings.

### Request body

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

### Response body

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

### Notes

- String input is normalized to a single-item list.
- Output is ordered by `index`.
- `usage` fields are placeholder `0` in baseline release.

### Error contract

```json
{
  "error": {
    "message": "invalid input",
    "type": "invalid_request_error",
    "param": "input",
    "code": "invalid_input"
  }
}
```
