#!/usr/bin/env bash
# Open an SSH tunnel to a running Grace vLLM job.
# Assumes the Slurm job is already RUNNING (start it manually with sbatch first).
#
# Usage:
#   ./developer_scripts/start_grace_gemma_tunnel.sh [--variant <model-id>]
#
# Known variants:
#   grace-gemma-4-31b           (bf16, port 8001, 2× A100)
#   grace-gemma-4-31b-fp8       (FP8,  port 8002, 1× A100)
#   grace-gemma-4-26b-a4b-fp8  (FP8,  port 8003, 1× A100)
#
# Two Duo prompts are expected — one to discover the compute node, one to open the tunnel.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${REPO_ROOT}/.env"

# ── Defaults ──────────────────────────────────────────────────────────────────
VARIANT="grace-gemma-4-31b-fp8"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --variant)   VARIANT="${2:?--variant requires a value}"; shift 2 ;;
    --variant=*) VARIANT="${1#--variant=}"; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── Load .env ─────────────────────────────────────────────────────────────────
if [[ -f "${ENV_FILE}" ]]; then
  set -a
  source <(grep -v '^\s*#' "${ENV_FILE}" | grep -v '^\s*$' | sed 's/\r$//')
  set +a
fi

GRACE_SSH_HOST="${GRACE_SSH_HOST:-grace.hprc.tamu.edu}"
GRACE_SSH_USER="${GRACE_SSH_USER:-${USER:-$(whoami)}}"
GRACE_SSH_USER="${GRACE_SSH_USER#AUTH+}"
GRACE_SSH_USER="${GRACE_SSH_USER#auth+}"
VLLM_API_KEY="${VLLM_API_KEY:-grace-gemma4-local}"
POLL_INTERVAL_SEC="${POLL_INTERVAL_SEC:-15}"
WAIT_TIMEOUT_SEC="${WAIT_TIMEOUT_SEC:-1200}"

# ── Per-variant config ─────────────────────────────────────────────────────────
case "${VARIANT}" in
  grace-gemma-4-31b)
    JOB_NAME="gemma4-31b-vllm"
    LOCAL_PORT=8001 ;;
  grace-gemma-4-31b-fp8)
    JOB_NAME="gemma4-31b-quant-vllm"
    LOCAL_PORT=8002 ;;
  grace-gemma-4-26b-a4b-fp8)
    JOB_NAME="gemma4-26b-a4b-quant-vllm"
    LOCAL_PORT=8003 ;;
  *)
    echo "Unknown --variant '${VARIANT}'." >&2
    echo "Known: grace-gemma-4-31b, grace-gemma-4-31b-fp8, grace-gemma-4-26b-a4b-fp8" >&2
    exit 1 ;;
esac

REMOTE_PORT="${GRACE_REMOTE_PORT:-8000}"
MODELS_URL="http://localhost:${LOCAL_PORT}/v1/models"
PID_FILE="${SCRIPT_DIR}/.grace_tunnel_${VARIANT//[^a-zA-Z0-9]/_}.pid"

echo "========================================"
echo "Variant : ${VARIANT}"
echo "Job name: ${JOB_NAME}"
echo "Tunnel  : localhost:${LOCAL_PORT} -> <node>:${REMOTE_PORT}"
echo "========================================"
echo ""

# ── Step 1: discover compute node (Duo prompt #1) ─────────────────────────────
echo "[1/2] Looking up running node for '${JOB_NAME}' on Grace..."
echo "      (Duo authentication #1 expected)"
echo ""

NODE="$(
  ssh -o ConnectTimeout=30 "${GRACE_SSH_USER}@${GRACE_SSH_HOST}" \
    squeue -u "${GRACE_SSH_USER}" -h -n "${JOB_NAME}" -t RUNNING -o "%N" 2>/dev/null \
  | head -n1 \
  | sed 's/\[//g; s/\]//g; s/,.*//; s/^[[:space:]]*//; s/[[:space:]]*$//'
)"

if [[ -z "${NODE}" ]]; then
  echo ""
  echo "ERROR: No RUNNING job named '${JOB_NAME}' found." >&2
  echo "       Submit the job manually first, wait until it is RUNNING, then re-run this script." >&2
  exit 1
fi

echo "Compute node: ${NODE}"
echo ""

# ── Kill any existing tunnel on this port ─────────────────────────────────────
if [[ -f "${PID_FILE}" ]]; then
  old_pid="$(cat "${PID_FILE}")"
  if kill -0 "${old_pid}" 2>/dev/null; then
    echo "Stopping previous tunnel (pid ${old_pid})..."
    kill "${old_pid}" 2>/dev/null || true
    sleep 1
  fi
  rm -f "${PID_FILE}"
fi

# ── Step 2: open tunnel (Duo prompt #2) ───────────────────────────────────────
echo "[2/2] Opening SSH tunnel localhost:${LOCAL_PORT} -> ${NODE}:${REMOTE_PORT}"
echo "      (Duo authentication #2 expected)"
echo ""

ssh -N \
  -o ConnectTimeout=30 \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=60 \
  -L "${LOCAL_PORT}:${NODE}:${REMOTE_PORT}" \
  "${GRACE_SSH_USER}@${GRACE_SSH_HOST}" &
TUNNEL_PID=$!
echo "${TUNNEL_PID}" > "${PID_FILE}"
echo "Tunnel PID: ${TUNNEL_PID}"
echo ""

# ── Poll until vLLM API is ready ──────────────────────────────────────────────
echo "Waiting for vLLM API at ${MODELS_URL} (up to $((WAIT_TIMEOUT_SEC / 60)) min)..."
DEADLINE=$((SECONDS + WAIT_TIMEOUT_SEC))

while true; do
  if curl -sf -H "Authorization: Bearer ${VLLM_API_KEY}" "${MODELS_URL}" >/dev/null 2>&1; then
    echo ""
    echo "========================================"
    echo "Ready!  Model: ${VARIANT}"
    echo "  1. Open RADIANT-LLM UI"
    echo "  2. Select model: ${VARIANT}"
    echo "  3. Click Initialize"
    echo ""
    echo "Stop tunnel: ./developer_scripts/stop_grace_gemma_tunnel.sh --variant ${VARIANT}"
    echo "========================================"
    exit 0
  fi

  if ! kill -0 "${TUNNEL_PID}" 2>/dev/null; then
    echo "" >&2
    echo "ERROR: SSH tunnel exited unexpectedly. Check for port conflicts:" >&2
    echo "       netstat -ano | findstr :${LOCAL_PORT}" >&2
    rm -f "${PID_FILE}"
    exit 1
  fi

  if (( SECONDS > DEADLINE )); then
    echo "" >&2
    echo "ERROR: Timed out waiting for vLLM API. Check job log on Grace." >&2
    exit 1
  fi

  printf "."
  sleep "${POLL_INTERVAL_SEC}"
done
