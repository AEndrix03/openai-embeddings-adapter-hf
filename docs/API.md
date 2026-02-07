# API Contract

## POST /v1/embeddings

OpenAI-compatible endpoint for embeddings.

### Request body

```json
{
  "input": "hello world",
  "model": "optional-model-name",
  "dimensions": 384,
  "encoding_format": "float",
  "user": "optional-user"
}
```

- `input`: string or list of strings
- `dimensions`: optional requested output dimensions

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
