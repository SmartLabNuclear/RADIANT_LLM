#!/bin/bash
# RADIANT-LLM -- start script (auto-detects GPU, no manual -f flags needed)
#
# Usage: ./start.sh
#
# Replaces plain `docker compose up -d`. Automatically applies
# docker-compose.gpu.yml when an NVIDIA GPU is present on this machine
# (detected via `nvidia-smi`), otherwise starts CPU-only -- either way,
# a single command, no flags to remember.
#
# Always operates on the compose files sitting next to this script, so it
# works the same whether you're sitting in this folder or invoking it by
# full path from somewhere else.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_ARGS=(-f "$SCRIPT_DIR/docker-compose.yml")

if command -v nvidia-smi >/dev/null 2>&1; then
    echo "GPU detected -- starting with GPU acceleration"
    COMPOSE_ARGS+=(-f "$SCRIPT_DIR/docker-compose.gpu.yml")
else
    echo "No GPU detected -- starting CPU-only"
fi

docker compose "${COMPOSE_ARGS[@]}" up -d
