#!/usr/bin/env bash
# Stop local SSH tunnel(s) to Grace vLLM (does not cancel the Slurm job).
# Usage: ./developer_scripts/stop_grace_gemma_tunnel.sh [--variant <model-id>] [--all]
#   --variant defaults to grace-gemma-4-31b (today's behavior, unchanged).
#   --all stops every known tunnel (all PID files under developer_scripts/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VARIANT="grace-gemma-4-31b"
STOP_ALL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --variant) VARIANT="${2:?--variant requires a value}"; shift 2 ;;
    --variant=*) VARIANT="${1#--variant=}"; shift ;;
    --all) STOP_ALL=1; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

stop_pid_file() {
  local pid_file="$1"
  if [[ ! -f "${pid_file}" ]]; then
    echo "No tunnel pid file at ${pid_file}"
    return 0
  fi
  local pid
  pid="$(cat "${pid_file}")"
  if kill -0 "${pid}" 2>/dev/null; then
    echo "Stopping SSH tunnel (pid ${pid}, ${pid_file})..."
    kill "${pid}" 2>/dev/null || true
    sleep 1
  else
    echo "Tunnel process ${pid} is not running."
  fi
  rm -f "${pid_file}"
}

if [[ "${STOP_ALL}" -eq 1 ]]; then
  found=0
  for pid_file in "${SCRIPT_DIR}"/.grace_tunnel_*.pid; do
    [[ -e "${pid_file}" ]] || continue
    found=1
    stop_pid_file "${pid_file}"
  done
  if [[ "${found}" -eq 0 ]]; then
    echo "No tunnel pid files found in ${SCRIPT_DIR}"
  fi
else
  SAFE_VARIANT="${VARIANT//[^a-zA-Z0-9]/_}"
  stop_pid_file "${SCRIPT_DIR}/.grace_tunnel_${SAFE_VARIANT}.pid"
fi

echo "Done. Slurm job(s) on Grace are unchanged."
