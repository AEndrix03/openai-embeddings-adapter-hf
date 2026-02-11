# Deployment Guide

## Docker (CPU)

```bash
docker build -f Dockerfile.cpu -t hf-adapter:cpu .
docker run --rm -p 8000:8000 --env-file .env.example hf-adapter:cpu
```

## Docker (CUDA)

```bash
docker build -f Dockerfile.gpu -t hf-adapter:cuda .
docker run --rm --gpus all -p 8000:8000 --env-file .env.example hf-adapter:cuda
```

## Docker (ROCm 6)

```bash
docker build \
  --build-arg TORCH_BASE_IMAGE=rocm/pytorch:rocm6.4_ubuntu24.04_py3.12_pytorch_release_2.4.1 \
  -f Dockerfile.gpu -t hf-adapter:rocm6 .
docker run --rm \
  --device=/dev/kfd --device=/dev/dri \
  --group-add=video --group-add=render \
  --security-opt seccomp=unconfined \
  -p 8000:8000 --env-file .env.example hf-adapter:rocm6
```

## Docker Compose profiles

```bash
docker compose --profile cpu up --build
docker compose --profile cuda up --build adapter-cuda
docker compose --profile rocm6 up --build adapter-rocm6
```

`adapter-cuda` requires a CUDA-capable runtime (NVIDIA driver + NVIDIA Container Toolkit).

`adapter-rocm6` requires ROCm devices exposed to containers (`/dev/kfd` and `/dev/dri`).

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
