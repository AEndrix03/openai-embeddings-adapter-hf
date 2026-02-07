# Security

## Authentication

Supported modes via environment:

- `none`
- `bearer`
- `basic`

Authentication is enforced at middleware level before request processing.

## Rate limiting

Token bucket rate limiting is available to protect shared/GPU services.

## Hardening

- Non-root containers
- Security scans in CI
- SBOM generation
