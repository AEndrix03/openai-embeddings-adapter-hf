# Runbook

## Graceful shutdown and drain

When SIGTERM is received:

1. Drain mode is enabled.
2. `/readyz` reports not ready.
3. New requests are rejected with `503` retryable error.
4. In-flight requests are allowed to complete up to `ADAPTER_DRAIN_TIMEOUT_SECONDS`.

## Troubleshooting quick list

- 503 spikes: check drain events and rollout settings.
- 429 spikes: tune `ADAPTER_RATE_LIMIT_RPS` and burst.
- slow startup: warm model or enable eager loading.
- OOM: reduce max batch/length and use stricter limits.
