# Deployment

## Docker

Use either CPU or GPU image variants and pass environment from `.env.example`.

## Kubernetes

- Configure readiness/liveness probes to `/readyz` and `/livez`.
- Use rolling updates with maxUnavailable tuned to avoid full downtime.
- During SIGTERM, pod enters drain mode and should be removed from service endpoints.
