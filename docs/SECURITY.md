# Security

## Threat model

Primary risks:

- unauthorized access
- abusive request rates
- oversized input leading to resource exhaustion
- vulnerable dependencies/images

## Controls

- Authentication (`none`/`bearer`/`basic`)
- Token-bucket rate limiting
- Input limits (batch, per-item chars, total chars)
- Graceful drain behavior for safe rollouts
- Non-root containers

## CI security checks

- dependency audit (`pip-audit`)
- container vulnerability scan (`trivy`)
- SBOM generation (`syft`/SPDX)

## Secrets and least privilege

- pass secrets through secure env/secret manager
- avoid logging secrets
- keep runtime permissions minimal
