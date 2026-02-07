# Observability Guide

## Logs

Structured logs include request id, route, method, status, and latency.
Enable JSON with `ADAPTER_LOG_JSON=true`.

## Metrics

Endpoint: `/metrics` (if enabled).

Key metrics:

- `adapter_http_requests_total`
- `adapter_http_request_latency_seconds`
- `adapter_embed_requests_total`
- `adapter_embed_duration_seconds`
- `adapter_model_loaded`
- `adapter_drain_mode`

ServiceMonitor manifest: `k8s/base/servicemonitor.yaml`.

## Tracing

Enable OTLP export with:

- `ADAPTER_OTEL_ENABLED=true`
- `ADAPTER_OTEL_ENDPOINT=...`

Resource attributes:

- `service.name`
- `adapter.model_id`
- `adapter.device`

## Correlation

Use `X-Request-Id` to correlate logs and traces across systems.

## Dashboard suggestions

- request volume by route
- p50/p95/p99 latency
- 4xx/5xx split
- 429 trend
- embedding duration trend

## Alerting suggestions

- 5xx rate above threshold
- p95 latency sustained high
- drain mode unexpectedly long
