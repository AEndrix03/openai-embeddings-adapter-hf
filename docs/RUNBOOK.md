# Operational Runbook

## Suggested SLOs

- Availability: 99.9%
- p95 latency: < 500ms (small batches)
- Error budget focused on 5xx and 429 behavior

## Drain and shutdown

On SIGTERM:

1. drain mode enabled
2. `/readyz` reports not-ready
3. new requests return `503`
4. in-flight requests complete within timeout

## Incident playbooks

### 503 / timeout spikes

- Check deployment rollouts and pod terminations.
- Verify drain timeout and readiness probe delays.
- Inspect model loading latency and upstream resource pressure.

### OOM events

- Lower `ADAPTER_MAX_BATCH_SIZE`.
- Lower `ADAPTER_MAX_LENGTH_TOKENS`.
- Keep strict input limits enabled.

### 429 bursts

- Increase capacity or replicas.
- Tune rate limit RPS/burst.
- Apply backoff/retry policy in callers.

### dimensions mismatch

- Align request `dimensions` and `X-Embedding-Dim` with model capability.
- Remove conflicting hint headers.

### cache issues / slow model load

- Verify HF cache volume/PVC mount.
- Ensure model artifacts are cached and persistent.
