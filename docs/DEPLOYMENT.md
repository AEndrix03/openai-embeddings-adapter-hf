# Deployment Guide

## Docker (CPU)

```bash
docker build -f Dockerfile.cpu -t hf-adapter:cpu .
docker run --rm -p 8000:8000 --env-file .env.example hf-adapter:cpu
```

## Docker (GPU)

```bash
docker build -f Dockerfile.gpu -t hf-adapter:gpu .
docker run --rm --gpus all -p 8000:8000 --env-file .env.example hf-adapter:gpu
```

## Docker Compose profiles

```bash
docker compose --profile cpu up --build
docker compose --profile gpu up --build
```

## Kubernetes base

```bash
kubectl apply -k k8s/
```

## Kubernetes overlays

```bash
kubectl apply -k k8s/overlays/cpu
kubectl apply -k k8s/overlays/gpu
```

## Environment configuration

Set model/runtime/auth/limits using env vars from `.env.example`.
Key startup/cache variables:

- `ADAPTER_LOAD_MODEL_ON_STARTUP=true|false` preload model at container start
- `ADAPTER_CACHE_ENABLED=true|false` enable response cache
- `ADAPTER_CACHE_PATH=/var/cache/adapter/embeddings_cache.sqlite3`
- `ADAPTER_CACHE_MAX_ENTRIES=<int>`

## Rollout checks

```bash
kubectl rollout status deploy/hf-embeddings-adapter
kubectl get pods -l app=hf-embeddings-adapter
```

## GPU requirements

- NVIDIA driver and container runtime
- Kubernetes NVIDIA device plugin
- Persistent volume claim `hf-embeddings-adapter-cache-pvc` for response cache
