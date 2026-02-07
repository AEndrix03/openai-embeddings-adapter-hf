# Security and Hardening

## Threat model

Primary risks:

- unauthorized access
- abusive rates / denial-of-service
- oversized payloads causing memory pressure
- vulnerable dependencies/images

## Authentication modes

- `none`
- `bearer`
- `basic`

## Request protections

- rate limit token bucket (`429`)
- input validation and text limits (`400`)
- model hint mismatch rejection (`400`)

## Operational headers

- `X-Request-Id` for traceability
- CPM hint headers are parsed and validated

## Secret management

- inject credentials via secret stores or environment at deploy time
- do not commit secrets
- avoid logging secret values

## Runtime hardening

- non-root containers
- limited resource requests/limits
- graceful drain on SIGTERM

## Supply chain controls

- dependency audit (`pip-audit`)
- image scan (`trivy`)
- SBOM artifact (`syft`/SPDX)

## Least privilege

- minimum RBAC on Kubernetes
- minimum registry/token permissions in CI
