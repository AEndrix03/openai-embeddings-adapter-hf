# Deployment

## Docker

Use either CPU or GPU image variants and pass environment from `.env.example`.

## Kubernetes

### Base install

```bash
kubectl apply -k k8s/
```

### Rollout

```bash
kubectl rollout status deploy/hf-embeddings-adapter
```

### Probes and drain

- readiness: `/readyz`
- liveness: `/livez`
- health: `/healthz`

Use rolling update strategy and keep at least one replica available.

## GPU requirements

- NVIDIA driver and container runtime must be installed on host/cluster nodes.
- Kubernetes GPU scheduling requires NVIDIA device plugin.
