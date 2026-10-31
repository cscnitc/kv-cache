#!/usr/bin/env bash
# How the vLLM server is set up. Needs Linux, NVIDIA driver, Docker, NVIDIA Container Toolkit.
set -euo pipefail
cd "$(dirname "$0")"

nvidia-smi                                   # must show GPU + driver before anything else
docker compose pull
docker run --rm --gpus all --entrypoint nvidia-smi vllm/vllm-openai:latest -L   # GPU visible in container
docker compose up -d

until curl -sf localhost:8000/health; do sleep 3; done   # wait for server
curl -s localhost:8000/v1/models; echo

# --- Colab/Kaggle (no Docker): run instead of the docker lines above ---
#   pip install uv && uv venv && uv pip install vllm
#   .venv/bin/vllm serve Qwen/Qwen2.5-1.5B-Instruct --served-model-name qwen2.5-1.5b \
#       --max-model-len 4096 --dtype half --enable-prefix-caching &
