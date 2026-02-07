# Performance

## Prerequisites

Install `hey` for basic load testing.

## Load test

```bash
scripts/load_test.sh http://localhost:8000 10 100
```

## Tuning

- `ADAPTER_MAX_BATCH_SIZE`
- `ADAPTER_MAX_LENGTH_TOKENS`
- `ADAPTER_MODEL_DTYPE`
- `ADAPTER_RATE_LIMIT_RPS`
- `ADAPTER_RATE_LIMIT_BURST`

## Notes

- Start with conservative batch sizes for GPU memory safety.
- Keep limits enabled to prevent abusive input.
- Use tracing/metrics to identify latency bottlenecks.
