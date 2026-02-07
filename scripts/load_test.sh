#!/usr/bin/env bash
set -euo pipefail

if ! command -v hey >/dev/null 2>&1; then
  echo "hey is required: https://github.com/rakyll/hey"
  exit 1
fi

BASE_URL="${1:-http://localhost:8000}"
CONCURRENCY="${2:-10}"
REQUESTS="${3:-100}"

hey -n "$REQUESTS" -c "$CONCURRENCY" -m POST \
  -H "Content-Type: application/json" \
  -d '{"input":["hello","world"]}' \
  "$BASE_URL/v1/embeddings"
