#!/usr/bin/env bash
# RADIANT-LLM: One-time Grace HPC setup script.
# Run ON a Grace login node after SSH login — not from your local machine.
#
# Usage:
#   bash developer_scripts/setup_grace.sh --hf-token hf_xxxx
#   bash developer_scripts/setup_grace.sh --hf-token hf_xxxx --base-dir /scratch/user/netid/llm
#   bash developer_scripts/setup_grace.sh --skip-download --skip-venv   # re-generate sbatch only
#
# Flags:
#   --hf-token TOKEN     HuggingFace token (required for model downloads)
#   --base-dir PATH      Root directory for all RADIANT-LLM files on this cluster
#                        (default: /scratch/user/$USER/local_llm)
#   --models LIST        Comma-separated checkpoints to download: 31b,26b-a4b
#                        (default: both)
#   --skip-venv          Skip Python venv creation (reuse existing)
#   --skip-download      Skip model downloads
#   --force-sbatch       Overwrite existing sbatch files
#   --no-modules         Skip 'module load' calls (for non-Grace HPRC clusters)
#
# Prerequisites (accept BEFORE running — requires HuggingFace account):
#   https://huggingface.co/google/gemma-4-26B-A4B-it
#   https://huggingface.co/google/gemma-4-31B-it
#
# After this script completes, add to your LOCAL .env (on your own machine):
#   GRACE_SSH_USER=<your_netid>
#   GRACE_MODELS_DIR=<base-dir>/models
set -euo pipefail

# ── defaults ──────────────────────────────────────────────────────────────────
NETID="${USER:-$(whoami)}"
BASE_DIR="/scratch/user/${NETID}/local_llm"
HF_TOKEN=""
SKIP_VENV=0
SKIP_DOWNLOAD=0
FORCE_SBATCH=0
NO_MODULES=0
MODELS_ARG="31b,26b-a4b"

# ── arg parse ─────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --hf-token)      HF_TOKEN="${2:?--hf-token requires a value}"; shift 2 ;;
    --hf-token=*)    HF_TOKEN="${1#--hf-token=}"; shift ;;
    --base-dir)      BASE_DIR="${2:?--base-dir requires a value}"; shift 2 ;;
    --base-dir=*)    BASE_DIR="${1#--base-dir=}"; shift ;;
    --models)        MODELS_ARG="${2:?--models requires a value}"; shift 2 ;;
    --models=*)      MODELS_ARG="${1#--models=}"; shift ;;
    --skip-venv)     SKIP_VENV=1; shift ;;
    --skip-download) SKIP_DOWNLOAD=1; shift ;;
    --force-sbatch)  FORCE_SBATCH=1; shift ;;
    --no-modules)    NO_MODULES=1; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── derived paths ─────────────────────────────────────────────────────────────
MODELS_DIR="${BASE_DIR}/models"
JOBS_DIR="${BASE_DIR}/jobs"
LOGS_DIR="${BASE_DIR}/logs"
TMP_DIR="${BASE_DIR}/tmp"
HF_CACHE="${BASE_DIR}/hf_cache"
VENV_DIR="${BASE_DIR}/envs/vllm_gemma4_venv"

echo "=== RADIANT-LLM Grace HPC Setup ==="
echo "  Netid    : ${NETID}"
echo "  Base dir : ${BASE_DIR}"
echo ""

# ── step 1: directories ───────────────────────────────────────────────────────
echo "[1/4] Creating directory structure..."
mkdir -p \
  "${MODELS_DIR}" \
  "${JOBS_DIR}" \
  "${LOGS_DIR}" \
  "${TMP_DIR}" \
  "${HF_CACHE}/hub" \
  "${HF_CACHE}/transformers" \
  "${BASE_DIR}/envs"
echo "  OK"

# ── step 2: python venv + vLLM ────────────────────────────────────────────────
echo ""
echo "[2/4] Python venv + vLLM..."

if [[ "${SKIP_VENV}" -eq 0 ]]; then
  if [[ "${NO_MODULES}" -eq 0 ]]; then
    module load GCCcore/13.3.0 Python/3.12.3 CUDA/12.4.1 2>/dev/null \
      || echo "  WARNING: 'module load' failed — continuing (non-Grace cluster?)"
  fi

  if [[ -d "${VENV_DIR}" && -f "${VENV_DIR}/bin/python" ]]; then
    echo "  Skipping: venv already exists at ${VENV_DIR}"
  else
    echo "  Creating venv at ${VENV_DIR} ..."
    python3 -m venv "${VENV_DIR}"
    source "${VENV_DIR}/bin/activate"
    pip install --upgrade pip --quiet
    echo "  Installing vLLM 0.21.0 (this takes a few minutes)..."
    pip install "vllm==0.21.0" "huggingface_hub[cli]" --quiet
    echo "  OK: venv created"
  fi
else
  echo "  Skipping (--skip-venv)"
fi

# activate venv for hf download in step 3
if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  source "${VENV_DIR}/bin/activate"
fi

# ── step 3: model downloads ───────────────────────────────────────────────────
echo ""
echo "[3/4] Model downloads..."

if [[ "${SKIP_DOWNLOAD}" -eq 1 ]]; then
  echo "  Skipping (--skip-download)"
else
  if [[ -z "${HF_TOKEN}" ]]; then
    echo "  Skipping: --hf-token not provided."
    echo "  Re-run with --hf-token hf_xxxx after accepting Gemma licenses."
  else
    IFS=',' read -ra SELECTED_MODELS <<< "${MODELS_ARG}"
    for model_key in "${SELECTED_MODELS[@]}"; do
      model_key="${model_key// /}"   # trim spaces
      case "${model_key}" in
        31b)      HF_REPO="google/gemma-4-31B-it";     FOLDER="gemma-4-31B-it" ;;
        26b-a4b)  HF_REPO="google/gemma-4-26B-A4B-it"; FOLDER="gemma-4-26B-A4B-it" ;;
        *) echo "  Unknown model key '${model_key}' — skipping (valid: 31b, 26b-a4b)"; continue ;;
      esac

      DEST="${MODELS_DIR}/${FOLDER}"
      if [[ -f "${DEST}/config.json" ]]; then
        echo "  Skipping ${FOLDER}: already downloaded (config.json present)"
      else
        echo "  Downloading ${HF_REPO} → ${DEST} ..."
        mkdir -p "${DEST}"
        HF_HOME="${HF_CACHE}" hf download "${HF_REPO}" \
          --local-dir "${DEST}" \
          --token "${HF_TOKEN}"
        echo "  OK: ${FOLDER}"
      fi
    done
    unset HF_TOKEN   # clear from env after use
  fi
fi

# ── step 4: sbatch files ──────────────────────────────────────────────────────
echo ""
echo "[4/4] Generating sbatch job files..."

write_sbatch() {
  local path="$1"
  local name
  name="$(basename "${path}")"
  if [[ -f "${path}" && "${FORCE_SBATCH}" -eq 0 ]]; then
    echo "  Skipping (exists): ${name}  — use --force-sbatch to overwrite"
    return
  fi
  cat > "${path}"
  echo "  OK: ${name}"
}

# --- 31B bf16 (TP=2, both A100s) ---
write_sbatch "${JOBS_DIR}/run_gemma4_31b_vllm.sbatch" << EOF
#!/bin/bash
#SBATCH --job-name=gemma4-31b-vllm
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=180G
#SBATCH --time=04:00:00
#SBATCH --output=${LOGS_DIR}/gemma4-31b-vllm.%j.out
#SBATCH --error=${LOGS_DIR}/gemma4-31b-vllm.%j.err

cd ${BASE_DIR}
module load GCCcore/13.3.0
module load Python/3.12.3
module load CUDA/12.4.1
source ${VENV_DIR}/bin/activate
export HF_HOME=${HF_CACHE}
export HF_HUB_CACHE=${HF_CACHE}/hub
export TRANSFORMERS_CACHE=${HF_CACHE}/transformers
export TMPDIR=${TMP_DIR}
export VLLM_API_KEY=grace-gemma4-local
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export PYTHONUNBUFFERED=1
echo "Running on node: \$(hostname)"
nvidia-smi
echo "Starting vLLM serve (31B bf16 TP=2) at \$(date)"
vllm serve ${MODELS_DIR}/gemma-4-31B-it \\
  --host 0.0.0.0 --port 8000 --api-key "\$VLLM_API_KEY" \\
  --tensor-parallel-size 2 --dtype bfloat16 \\
  --max-model-len 4096 --max-num-batched-tokens 4096 \\
  --gpu-memory-utilization 0.85 --enforce-eager --trust-remote-code \\
  --enable-auto-tool-choice --tool-call-parser gemma4
EOF

# --- 31B FP8 (TP=1, 1x A100) ---
write_sbatch "${JOBS_DIR}/run_gemma4_31b_quant_vllm.sbatch" << EOF
#!/bin/bash
#SBATCH --job-name=gemma4-31b-quant-vllm
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=120G
#SBATCH --time=04:00:00
#SBATCH --output=${LOGS_DIR}/gemma4-31b-quant-vllm.%j.out
#SBATCH --error=${LOGS_DIR}/gemma4-31b-quant-vllm.%j.err

cd ${BASE_DIR}
module load GCCcore/13.3.0
module load Python/3.12.3
module load CUDA/12.4.1
source ${VENV_DIR}/bin/activate
export HF_HOME=${HF_CACHE}
export HF_HUB_CACHE=${HF_CACHE}/hub
export TRANSFORMERS_CACHE=${HF_CACHE}/transformers
export TMPDIR=${TMP_DIR}
export VLLM_API_KEY=grace-gemma4-local
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export PYTHONUNBUFFERED=1
echo "Running on node: \$(hostname)"
nvidia-smi
echo "Starting vLLM serve (31B FP8 TP=1) at \$(date)"
vllm serve ${MODELS_DIR}/gemma-4-31B-it \\
  --host 0.0.0.0 --port 8000 --api-key "\$VLLM_API_KEY" \\
  --tensor-parallel-size 1 --quantization fp8 --dtype bfloat16 \\
  --max-model-len 16384 --max-num-batched-tokens 16384 \\
  --gpu-memory-utilization 0.85 --enforce-eager --trust-remote-code \\
  --enable-auto-tool-choice --tool-call-parser gemma4
EOF

# --- 26B-A4B FP8 (TP=1, 1x A100) ---
write_sbatch "${JOBS_DIR}/run_gemma4_26b_a4b_quant_vllm.sbatch" << EOF
#!/bin/bash
#SBATCH --job-name=gemma4-26b-a4b-quant-vllm
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=120G
#SBATCH --time=04:00:00
#SBATCH --output=${LOGS_DIR}/gemma4-26b-a4b-quant-vllm.%j.out
#SBATCH --error=${LOGS_DIR}/gemma4-26b-a4b-quant-vllm.%j.err

cd ${BASE_DIR}
module load GCCcore/13.3.0
module load Python/3.12.3
module load CUDA/12.4.1
source ${VENV_DIR}/bin/activate
export HF_HOME=${HF_CACHE}
export HF_HUB_CACHE=${HF_CACHE}/hub
export TRANSFORMERS_CACHE=${HF_CACHE}/transformers
export TMPDIR=${TMP_DIR}
export VLLM_API_KEY=grace-gemma4-local
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export PYTHONUNBUFFERED=1
echo "Running on node: \$(hostname)"
nvidia-smi
echo "Starting vLLM serve (26B-A4B FP8 TP=1) at \$(date)"
vllm serve ${MODELS_DIR}/gemma-4-26B-A4B-it \\
  --host 0.0.0.0 --port 8000 --api-key "\$VLLM_API_KEY" \\
  --tensor-parallel-size 1 --quantization fp8 --dtype bfloat16 \\
  --max-model-len 16384 --max-num-batched-tokens 16384 \\
  --gpu-memory-utilization 0.85 --enforce-eager --trust-remote-code \\
  --enable-auto-tool-choice --tool-call-parser gemma4
EOF

# ── done ──────────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup complete ==="
echo ""
echo "Add these lines to your LOCAL .env (on your own machine, not Grace):"
echo ""
echo "  GRACE_SSH_USER=${NETID}"
echo "  GRACE_MODELS_DIR=${MODELS_DIR}"
echo ""
echo "Then start a model tunnel from your local machine:"
echo "  ./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-26b-a4b-fp8"
echo "  ./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-31b-fp8"
echo ""
echo "Note: grace-gemma-4-31b (bf16) needs both A100s — do not run alongside the FP8 variants."
