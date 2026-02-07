#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"

curl -fsS "$BASE_URL/livez" >/dev/null
curl -fsS "$BASE_URL/readyz" >/dev/null
curl -fsS "$BASE_URL/healthz" >/dev/null

curl -fsS -X POST "$BASE_URL/v1/embeddings" \
  -H "Content-Type: application/json" \
  -d '{"input":"hello world"}' >/dev/null

echo "smoke-ok"
