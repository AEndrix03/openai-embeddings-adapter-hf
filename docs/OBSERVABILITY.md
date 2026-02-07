# Observability

## Logging

The adapter emits per-request structured logs including:

- request id
- route and method
- status code
- latency

Enable JSON logs with `ADAPTER_LOG_JSON=true`.

## Metrics

Prometheus endpoint is exposed on `/metrics` when `ADAPTER_METRICS_ENABLED=true`.

## Tracing

Enable tracing with:

- `ADAPTER_OTEL_ENABLED=true`
- `ADAPTER_OTEL_ENDPOINT=http://otel-collector:4318/v1/traces`

Resource attributes include service name, model id, and device.
