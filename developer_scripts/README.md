# RADIANT-LLM — Local Model Setup (Grace / HPRC)

This guide walks you through connecting a self-hosted Gemma 4 model running on an HPC cluster to RADIANT-LLM. When complete, local Grace models will appear alongside cloud models (GPT, Gemini) in the RADIANT model selector — no cloud API needed for inference.

> **Not on TAMU Grace?** The setup script and tunnel scripts work on any Slurm cluster with A100 GPUs. See [Section 12 — Non-Grace HPRC Clusters](#12-non-grace-hprc-clusters) for cluster-specific adjustments.

**Architecture overview:**

```
Your machine                Grace / HPRC cluster
┌─────────────┐  SSH tunnel  ┌──────────────────────────────┐
│  RADIANT-LLM│◄────────────►│  vLLM (Slurm GPU job)        │
│  (Docker /  │  port 8001+  │  Gemma 4 model (A100 GPU)    │
│   local)    │              └──────────────────────────────┘
└─────────────┘
```

RADIANT sends requests to `localhost:<port>` on your machine. The SSH tunnel forwards those to the [vLLM](https://docs.vllm.ai) server running on a GPU compute node inside the cluster. No model weights or GPU compute leave the cluster.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Get a HuggingFace Token](#2-get-a-huggingface-token)
3. [Accept Gemma Model Licenses](#3-accept-gemma-model-licenses)
4. [Transfer and Run the Setup Script](#4-transfer-and-run-the-setup-script)
5. [Configure Your Local .env](#5-configure-your-local-env)
6. [Start a Model Tunnel](#6-start-a-model-tunnel)
7. [Initialize the Model in RADIANT](#7-initialize-the-model-in-radiant)
8. [Model Variants Reference](#8-model-variants-reference)
9. [Running Multiple Variants Concurrently](#9-running-multiple-variants-concurrently)
10. [Stopping Tunnels](#10-stopping-tunnels)
11. [Monitoring and Logs](#11-monitoring-and-logs)
12. [Non-Grace HPRC Clusters](#12-non-grace-hprc-clusters)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Prerequisites

Before starting, confirm you have:

| Requirement | Notes |
|-------------|-------|
| HPC cluster account | Must have access to A100 GPUs via [Slurm](https://slurm.schedmd.com/documentation.html). This guide uses [TAMU Grace](https://hprc.tamu.edu/grace/) but the steps apply to any compatible cluster. |
| SSH access configured | `ssh your_netid@grace.hprc.tamu.edu` works from your machine |
| RADIANT-LLM codebase | Cloned and running locally (Docker or native) |
| ~200 GB free on scratch | For model weights + venv + cache |
| HuggingFace account | Free — needed for model license acceptance |

> **Cloud API users:** If you only use OpenAI or Gemini models, you can skip this entire guide. Grace setup is only needed for local inference.

---

## 2. Get a HuggingFace Token

1. Go to **[huggingface.co](https://huggingface.co)** and sign in (or create a free account)
2. Click your profile picture → **Settings** → **[Access Tokens](https://huggingface.co/settings/tokens)**
3. Click **New token** → name it (e.g. `grace-download`) → Role: **Read**
4. Copy the token — it starts with `hf_`

> **Security:** Never paste your HuggingFace token into scripts, Git files, chat messages, or log files. Pass it only as a command-line argument at runtime — the setup script accepts it via `--hf-token` and clears it from the environment after use.

---

## 3. Accept Gemma Model Licenses

Google requires a one-time license acceptance per model before your token can download it. While logged into HuggingFace, visit each model page and click **Agree and access repository**:

| Model | Page | Size | Used by variant |
|-------|------|------|-----------------|
| Gemma 4 26B-A4B | [google/gemma-4-26B-A4B-it](https://huggingface.co/google/gemma-4-26B-A4B-it) | ~52 GB | `grace-gemma-4-26b-a4b-fp8` |
| Gemma 4 31B | [google/gemma-4-31B-it](https://huggingface.co/google/gemma-4-31B-it) | ~62 GB | `grace-gemma-4-31b`, `grace-gemma-4-31b-fp8` |

License acceptance is per-account and permanent. You only do this once.

---

## 4. Transfer and Run the Setup Script

All cluster-side setup is handled by `setup_grace.sh`. It creates the directory structure, installs the Python venv with vLLM, downloads model checkpoints, and generates Slurm job files — all idempotent (safe to re-run).

### 4a. Copy the script to Grace

From your **local machine** (in the RADIANT-LLM repo root):

```bash
scp developer_scripts/setup_grace.sh your_netid@grace.hprc.tamu.edu:~/setup_grace.sh
```

Replace `your_netid` with your Grace username. You will be prompted for your password and Duo authentication.

### 4b. SSH into Grace

```bash
ssh your_netid@grace.hprc.tamu.edu
```

### 4c. Run the setup script

```bash
bash ~/setup_grace.sh --hf-token hf_xxxx
```

Replace `hf_xxxx` with your actual HuggingFace token from Step 2.

**To download only specific models** (saves time and storage):

```bash
# 26B-A4B only (~52 GB)
bash ~/setup_grace.sh --hf-token hf_xxxx --models 26b-a4b

# Both (default, ~114 GB total)
bash ~/setup_grace.sh --hf-token hf_xxxx --models 31b,26b-a4b
```

**For long downloads**, run inside `nohup` so it survives if your SSH session disconnects:

```bash
nohup bash ~/setup_grace.sh --hf-token hf_xxxx > ~/setup.log 2>&1 &
tail -f ~/setup.log
```

### 4d. What the script creates

After the script completes, you will have:

```
/scratch/user/your_netid/local_llm/
├── models/
│   ├── gemma-4-26B-A4B-it/      # ~52 GB
│   └── gemma-4-31B-it/          # ~62 GB
├── jobs/
│   ├── run_gemma4_26b_a4b_quant_vllm.sbatch
│   ├── run_gemma4_31b_quant_vllm.sbatch
│   └── run_gemma4_31b_vllm.sbatch
├── logs/                        # Slurm output files (created at job time)
├── envs/
│   └── vllm_gemma4_venv/        # Python venv with vLLM 0.21.0
├── hf_cache/                    # HuggingFace cache
└── tmp/
```

At the end the script prints the exact lines to add to your local `.env` — copy those before closing the terminal.

---

## 5. Configure Your Local .env

On your **local machine**, open the RADIANT-LLM `.env` file and add:

```env
# Grace / vLLM connection
VLLM_BASE_URL=http://localhost:8001/v1
VLLM_API_KEY=grace-gemma4-local
GRACE_SSH_USER=your_netid
GRACE_MODELS_DIR=/scratch/user/your_netid/local_llm/models
```

Replace `your_netid` with your actual Grace username. The `GRACE_MODELS_DIR` value is printed at the end of the setup script output.

> **VLLM_API_KEY** is a shared server key set inside the sbatch jobs — it is not your OpenAI or HuggingFace key. Do not reuse `OPENAI_API_KEY` here; vLLM will return 401.

---

## 6. Start a Model Tunnel

Starting a Grace model is a two-step process: first submit the Slurm job from Grace, then open the SSH tunnel from your local machine once the job is running. Grace queues are unpredictable — a job may start in 2 minutes or sit pending for over an hour — so separating submission from tunneling avoids long blocking waits.

### Step 1 — Submit the Slurm job (from Grace)

SSH into Grace and submit the sbatch file for the variant you want:

```bash
ssh your_netid@grace.hprc.tamu.edu

# 26B-A4B FP8 — recommended starting point
sbatch /scratch/user/your_netid/local_llm/jobs/run_gemma4_26b_a4b_quant_vllm.sbatch

# 31B FP8
sbatch /scratch/user/your_netid/local_llm/jobs/run_gemma4_31b_quant_vllm.sbatch

# 31B bf16 (2× A100 — do not run alongside any FP8 variant)
sbatch /scratch/user/your_netid/local_llm/jobs/run_gemma4_31b_vllm.sbatch
```

Check that the job was accepted and monitor its state:

```bash
squeue -u your_netid
```

Wait until the `STATE` column shows `R` (RUNNING). A job may sit in `PD` (pending) for minutes to over an hour depending on cluster load — this is normal. Note the node name in the `NODELIST` column for reference.

### Step 2 — Open the tunnel (from your local machine)

Once the job is RUNNING, open the SSH port-forward from your **local machine** (RADIANT-LLM repo root). Use `--no-submit` so the script connects immediately without re-submitting:

```bash
# 26B-A4B FP8
./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-26b-a4b-fp8 --no-submit

# 31B FP8
./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-31b-fp8 --no-submit

# 31B bf16
./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-31b --no-submit
```

The script will:
1. Prompt for your Grace password + Duo authentication **(first time — to locate the running job)**
2. Prompt for your Grace password + Duo authentication **(second time — to open the long-lived tunnel)**
3. Open the SSH tunnel in the background
4. Poll `localhost:<port>/v1/models` until vLLM is ready (~20–25 minutes from job start)
5. Print confirmation when ready

> **Two Duo prompts are expected.** The script uses two separate SSH sessions by design: one to find the compute node via `squeue`, and a second for the persistent tunnel. This avoids SSH multiplexing issues on Windows/Git Bash. Both prompts are normal — the second opens after the first completes.

> **Startup time:** vLLM takes roughly 20–25 minutes to fully load after the job reaches RUNNING. This is normal — it imports PyTorch, initializes CUDA, loads weights, and allocates KV cache before accepting requests.

> **Running in Docker?** The tunnel binds to `localhost:<port>` on your host machine. Inside the Docker container, use `host.docker.internal` instead of `localhost` to reach it. The `Docker_Executable/.env` in this repo already has this configured for all three variants — no extra steps needed.

When the script prints:
```
Ready for RADIANT-LLM:
  1. Open RADIANT UI
  2. Select model: grace-gemma-4-26b-a4b-fp8
  3. Click Initialize
```
the model is ready.

> **Auto-submit (optional):** Omitting `--no-submit` makes the tunnel script submit the job itself and wait for it to reach RUNNING before opening the tunnel. This works but requires the terminal to stay open for the full queue wait (potentially 1+ hour). Use the two-step approach above for reliability.

---

## 7. Initialize the Model in RADIANT

1. Open the RADIANT-LLM web UI
2. In the model selector dropdown, choose the Grace variant you started (e.g. **Grace Gemma 4 26B-A4B**)
3. Click **Initialize**
4. An info banner will confirm the model loaded with its context window size

You can now chat, use RAG, and run tools with the local model. Response quality may differ from cloud APIs — this is expected for self-hosted inference.

---

## 8. Model Variants Reference

| Variant ID | Display name | GPUs | Quantization | Context window | Notes |
|------------|-------------|------|-------------|----------------|-------|
| `grace-gemma-4-26b-a4b-fp8` | Grace Gemma 4 26B-A4B | 1× A100 | FP8 | 16,384 tokens | MoE architecture, competitive with larger dense models; recommended starting point |
| `grace-gemma-4-31b-fp8` | Grace Gemma 4 31B | 1× A100 | FP8 | 16,384 tokens | Full 31B dense, quantized |
| `grace-gemma-4-31b` | Grace Gemma 4 31B (bf16) | 2× A100 | None (full precision) | 4,096 tokens | Highest quality, uses both GPUs |

**FP8 quantization** reduces weight storage from 2 bytes to 1 byte per parameter using a software kernel (Marlin). On A100 GPUs this frees enough memory to run larger models on a single GPU and to support longer context windows. Quality loss is minimal in practice.

**Port assignments** (set automatically — no configuration needed unless you override):

| Variant | Local port |
|---------|-----------|
| `grace-gemma-4-31b` | 8001 |
| `grace-gemma-4-31b-fp8` | 8002 |
| `grace-gemma-4-26b-a4b-fp8` | 8003 |

---

## 9. Running Multiple Variants Concurrently

Each FP8 variant uses exactly **one A100**. Since Grace allocates one A100 per job and each job lands on a different node, you can run up to two FP8 variants simultaneously (one A100 per node × two nodes = two jobs).

**Step 1 — Submit both jobs from Grace:**

```bash
sbatch /scratch/user/your_netid/local_llm/jobs/run_gemma4_31b_quant_vllm.sbatch
sbatch /scratch/user/your_netid/local_llm/jobs/run_gemma4_26b_a4b_quant_vllm.sbatch
squeue -u your_netid   # wait until both show RUNNING
```

**Step 2 — Open a tunnel for each, in separate local terminals:**

```bash
# Terminal 1
./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-31b-fp8 --no-submit

# Terminal 2
./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-26b-a4b-fp8 --no-submit
```

Both tunnels stay open independently. Switch between models in RADIANT by changing the dropdown and clicking Initialize.

> **Important:** Do **not** run `grace-gemma-4-31b` (bf16, 2× A100) at the same time as any FP8 variant. Together they would request 4 GPUs from a 2-GPU allocation.

---

## 10. Stopping Tunnels

To stop a tunnel gracefully:

```bash
./developer_scripts/stop_grace_gemma_tunnel.sh --variant grace-gemma-4-26b-a4b-fp8
```

To stop all running Grace tunnels at once:

```bash
./developer_scripts/stop_grace_gemma_tunnel.sh --all
```

The underlying Slurm job continues running on Grace until its walltime ends (4 hours by default) or you cancel it manually:

```bash
ssh your_netid@grace.hprc.tamu.edu 'scancel -n gemma4-26b-a4b-quant-vllm'
```

---

## 11. Monitoring and Logs

**Check which jobs are running on Grace** (from your local machine):

```bash
ssh your_netid@grace.hprc.tamu.edu 'squeue -u your_netid'
```

**Watch the vLLM startup log in real time** (from a Grace login node):

```bash
# Replace <JOBID> with the actual job ID from squeue
tail -f /scratch/user/your_netid/local_llm/logs/gemma4-26b-a4b-quant-vllm.<JOBID>.out
```

Look for this line to confirm vLLM is ready:
```
INFO ... Uvicorn running on http://0.0.0.0:8000
```

**Verify the tunnel is working** (from your local machine, after the tunnel is open):

```bash
curl -sf -H "Authorization: Bearer grace-gemma4-local" http://localhost:8003/v1/models
```

A successful response is JSON containing the model path and `max_model_len`.

---

## 12. Non-Grace HPRC Clusters

The setup script and tunnel script work on any Slurm cluster with A100 GPUs, not just Grace. For clusters with different module systems, pass `--no-modules` to skip the `module load` calls and manage your Python environment manually:

```bash
bash ~/setup_grace.sh --hf-token hf_xxxx --no-modules
```

You will need to ensure Python 3.12+ and CUDA 12.4+ are available in your environment before running the script, and that the same environment is active when the sbatch jobs run (edit the generated sbatch files to replace `module load ...` with whatever your cluster requires).

Update your local `.env` to point to the correct SSH host:

```env
GRACE_SSH_HOST=your_cluster_login_node.edu
GRACE_SSH_USER=your_username
GRACE_MODELS_DIR=/path/to/your/models/dir
```

---

## 13. Troubleshooting

### vLLM never prints "Uvicorn running" — job disappears from queue

The job likely ran out of GPU memory (OOM) during KV cache pre-allocation. Check the job error log:

```bash
cat /scratch/user/your_netid/local_llm/logs/gemma4-<variant>.<JOBID>.err
```

**Fix:** Edit the sbatch file to reduce `--max-model-len`, then resubmit. Reduce by half each attempt:
```
--max-model-len 8192 --max-num-batched-tokens 8192
```

To regenerate sbatch files after editing, re-run the setup script with `--force-sbatch --skip-download --skip-venv`.

---

### curl returns 401 Unauthorized

The `VLLM_API_KEY` in your `.env` does not match the key set inside the sbatch file.

- The sbatch files generated by `setup_grace.sh` set `VLLM_API_KEY=grace-gemma4-local`
- Your `.env` must have `VLLM_API_KEY=grace-gemma4-local`
- Do **not** use `OPENAI_API_KEY` here

---

### Tunnel script times out waiting for Slurm job

The cluster queue may be busy. Check the job status:

```bash
ssh your_netid@grace.hprc.tamu.edu 'squeue -u your_netid'
```

If the job shows `PD` (pending), it is waiting for a free GPU — this is normal during high demand. Re-run the tunnel script with `--no-submit` once the job reaches `RUNNING`:

```bash
./developer_scripts/start_grace_gemma_tunnel.sh --variant grace-gemma-4-12b-fp8 --no-submit
```

---

### HuggingFace download fails with 401

You either have not accepted the model license or are using the wrong token.

1. Make sure you are logged into [huggingface.co](https://huggingface.co) and have clicked **Agree and access repository** on each model page (Step 3 above)
2. Confirm the token starts with `hf_` and has **Read** access
3. Re-run: `bash ~/setup_grace.sh --hf-token hf_xxxx --models 26b-a4b --skip-venv`

---

### "No running processes found" in nvidia-smi output

This appears in the log immediately after job start, before vLLM loads onto the GPU. It is **not an error** — the GPU is idle for the first few minutes while Python imports and model weights load. Wait for "Uvicorn running" (~20–25 min from job submission).

---

### Tunnel port already in use (Windows)

If the tunnel script or a manual `ssh -N -L` exits immediately with `bind [127.0.0.1]:<port>: Address already in use`, a previous tunnel process is still holding that port.

Find and kill it from Git Bash or PowerShell:

```bash
# Git Bash
netstat -ano | grep <port>          # note the PID in the last column
taskkill //PID <pid> //F
```

```powershell
# PowerShell
netstat -ano | findstr :<port>
taskkill /PID <pid> /F
```

Then re-run the tunnel command.

---

### Tool calling fails — model returns plain text instead of tool calls

The sbatch job is missing `--enable-auto-tool-choice` and `--tool-call-parser gemma4`. The files generated by `setup_grace.sh` include these flags. If you edited your sbatch files manually and removed them, add them back:

```
--enable-auto-tool-choice --tool-call-parser gemma4
```

Then `scancel` the job, `sbatch` again, and reopen the tunnel.

---
