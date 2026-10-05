# visual-parser (Standalone Visual-RAG PDF Ingestion)

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1%2B-ee4c2c.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-1C3C3C.svg)
![CUDA](https://img.shields.io/badge/CUDA-optional-76B900.svg)

`visual-parser` converts PDFs into a multi-modal JSONL knowledge base (text chunks, figure descriptions, metadata). It was extracted from [RADIANT-LLM](https://github.com/SmartLabNuclear/RADIANT_LLM) as a standalone PDF-ingestion tool, independent of any chatbot.

1) Run `visual-parser` on curated PDFs to generate JSONL KB files.
2) Point any downstream RAG system at the generated KB — RADIANT-LLM, AutoSAM, and AutoFLUKA all consume the identical JSONL/registry format, so the same KB works with any of them without re-parsing.

## Table of Contents

- [Outputs (JSONL KB)](#outputs-jsonl-kb)
- [API Keys (.env)](#api-keys-env)
- [Install and Run](#install-and-run)
  - [Via pip](#via-pip)
  - [Via Docker](#via-docker)
  - [From source](#from-source)
- [Common configuration flags](#common-configuration-flags)
- [Local Ollama vision provider](#local-ollama-vision-provider)
- [Citation](#citation)
- [License](#license)

## Outputs (JSONL KB)

By default, the pipeline writes:
- `01_chunks_kb.jsonl`: chunked text extracted from PDFs (Nougat by default).
- `02_visuals_kb.jsonl`: figure/page visual descriptions (Vision LLM).
- `03_metadata_kb.jsonl`: document metadata rows (title/author/etc.).

Alongside the KB, the pipeline also writes two bookkeeping files: `04_processed_pdfs.txt` (tracks which PDFs have already been processed, so re-runs skip them unless `--rebuild`) and `05_pipeline.log` (run log at the verbosity set by `--log-level`, default `ERROR`).

## API Keys (.env)

Provide at least one provider:
- `OPENAI_API_KEY` (OpenAI)
- `GEMINI_API_KEY` (Gemini)

Set these via a `.env` file (checked, in order: `~/.config/visual-parser/.env`, a `.env` in the current directory, `$VISUAL_PARSER_ENV_FILE` if set) or as regular OS environment variables (e.g. `setx` on Windows).

Optional:
- `HF_TOKEN` (for gated Hugging Face models)
- `PORTKEY_API_KEY` + `PORTKEY_OPENAI_PROVIDER_SLUG` — routes OpenAI-family calls (vision LLM + `--list-models`) through a [Portkey](https://portkey.ai) gateway instead of OpenAI directly. Only takes effect when `OPENAI_API_KEY` is absent/empty; direct OpenAI wins when both are set. Set `VISUAL_PARSER_FORCE_PORTKEY=true` to force Portkey even when `OPENAI_API_KEY` is set at the OS/system level.

## Install and Run

Three ways to run `visual-parser`, in order of setup effort: [pip install](#via-pip), [Docker](#via-docker), or [from source](#from-source). All three share the identical CLI and flags — see [Common configuration flags](#common-configuration-flags).

### Via pip

```bash
pip install visual-parser
```

Check the install:

```bash
visual-parser --version
```

Run against a folder of PDFs:

```bash
visual-parser --input-dir /path/to/pdfs --output-dir /path/to/pdfs
```

#### GPU acceleration

`--text-mode nougat` (the default) uses a CUDA GPU automatically when one is available (`torch.cuda.is_available()`). A plain `pip install visual-parser` (or `pip install torch`) installs PyPI's default CPU-only torch wheel, even on a GPU machine. Install the matching CUDA build from PyTorch's index instead:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu130
```

Use `cu130` or newer, not `cu126` — `cu126` only covers compute capability up to `sm_90` (Hopper); on a newer GPU (e.g. Blackwell, `sm_120`), `torch.cuda.is_available()` still reports `True` but the first kernel launch fails. `cu130` covers Blackwell and every architecture `cu126` covered, and requires an r580+ NVIDIA driver. Pick the exact tag for your driver at [pytorch.org/get-started](https://pytorch.org/get-started/locally/) if `cu130` doesn't apply. Reinstalling `visual-parser` afterward does not downgrade this back to CPU. Verify with:

```bash
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
```

### Via Docker

Prebuilt images are on **[zev94/radiant-llm](https://hub.docker.com/r/zev94/radiant-llm)** under the **visual-parser** tags:

| Tag | Description |
|-----|-------------|
| `visual-parser-latest` | Always latest build (rolling) |
| `visual-parser-2.1.0` | Pinned release |
| `visual-parser-2.0` | Pinned release |
| `visual-parser-1.0.2` | Legacy |
| `visual-parser-1.0` | Legacy — v1.0.0, stale |

#### Install Docker

Docker Desktop (Windows/macOS) or Docker Engine (Linux).

#### Pull the image

```bash
docker pull zev94/radiant-llm:visual-parser-latest
```

#### Run (input and output on the same mounted folder)

Windows PowerShell:
```powershell
docker run --rm --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data
```

Linux / WSL:
```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data
```

#### Run (separate output directory)

Windows PowerShell:
```powershell
docker run --rm --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  -v "C:\path\to\out:/out" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /out
```

#### GPU acceleration

Add `--gpus all` to any run command above to use an NVIDIA GPU instead of CPU for `--text-mode nougat` (the default). Works out of the box with Docker Desktop's WSL2 backend; no extra `nvidia-container-toolkit` install needed on most machines. Omit it (or run on a machine with no GPU) to fall back to CPU automatically.

Requires an NVIDIA driver supporting CUDA 13.0+ (r580 or newer) on the host — check with `nvidia-smi`; update from [nvidia.com/Download](https://www.nvidia.com/Download/index.aspx) if it reports an older version. Without it, `torch.cuda.is_available()` still reports `True`, but the first Nougat inference call fails with `CUDA error: no kernel image is available`:

```powershell
docker run --rm --gpus all --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data
```

#### Troubleshooting: GPU not detected

- Confirm the host sees the GPU at all: `nvidia-smi` (run from WSL if on Windows).
- Confirm the driver supports CUDA 13.0+: check the `CUDA Version` line in that output — needs to read 13.0 or higher (roughly r580+). Update from [nvidia.com/Download](https://www.nvidia.com/Download/index.aspx) if it reads lower.
- Confirm Docker can reach the GPU: `docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi`.
- If Docker Desktop's WSL2 backend still doesn't see the GPU after a driver update, restart the WSL VM: `wsl --shutdown`, then restart Docker Desktop.

#### Offline install (legacy .tar)

```powershell
docker load -i .\visual-parser_2.1.0.tar
docker images   # use the tag printed by Docker
```

#### Model overrides (optional)

Default vision model is **GPT-5.4** when using `--vision-provider gpt`. Override on the command line (works identically via Docker or a plain CLI install):

```powershell
docker run --rm --env-file .env -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data --vision-model gpt-5.6
```

### From source

Clone the repository and install dependencies directly, without packaging:

```bash
git clone https://github.com/SmartLabNuclear/RADIANT_LLM.git
cd RADIANT_LLM/Visual-Parser
pip install -r requirements.txt
```

Run the top-level script:

```bash
python visual-parser.py --input-dir ./my_pdfs
```

or as a module:

```bash
python -m visual_parser --input-dir ./my_pdfs
```

Both use the same CLI and flags as [Via pip](#via-pip). GPU acceleration follows the same rule: a plain `pip install -r requirements.txt` also resolves to the CPU-only torch wheel by default — see [GPU acceleration](#gpu-acceleration) under Via pip for the CUDA-build install command.

## Common configuration flags

Full flag list via `--help` — Docker:

```bash
docker run --rm zev94/radiant-llm:visual-parser-latest --help
```

or plain CLI:

```bash
visual-parser --help
```

For copy-paste Docker examples (vision presets, text modes, workers, rebuild), see [`docker-usage-examples.md`](docker-usage-examples.md).

Paths:
- `--input-dir` / `-i` (required unless `--list-models` is given)
- `--output-dir` / `-o` (default: same as input)

Text extraction:
- `--text-mode nougat|lightweight` (default: `nougat`)
- `--nougat-model facebook/nougat-small`
- `--chunk-size 500`
- `--chunk-overlap 100`

Vision LLM:
- `--vision-provider gpt|gemini|ollama` (default: `gpt`) — see [Local Ollama vision provider](#local-ollama-vision-provider) for the `ollama` option
- `--vision-model gpt-5.6` (or `gpt-4o`, `gemini-2.5-flash`, etc. — run `--list-models` for what's actually live on your account; omit entirely for `ollama` to auto-select)
- `--vision-detail low|high|auto` (default: `low`)
- `--reasoning-effort minimal|none|low|medium|high|xhigh` (default: `medium`)
- `--metadata-pages 2`
- `--vision-context-pages 0` — include N adjacent pages (before and after) as context in each figure-description call, to help with figures/captions that span a page break. 0 (default) is today's single-page behavior; more context pages means more tokens per call

Performance / misc:
- `--max-workers 4`
- `--rebuild` (reprocess everything; ignore `04_processed_pdfs.txt`)
- `--skip-text` (skip text extraction and resume only the vision steps; use after an interrupted run)
- `--list-models` — print the live, currently-available vision models for whichever provider(s) you have a key configured for, then exit (no PDF processing). Reflects Portkey's catalog too when that's active.
- `--version` / `-V`
- `--log-level DEBUG|INFO|WARNING|ERROR` (default: `ERROR`)

## Local Ollama vision provider

`--vision-provider ollama` runs figure description and metadata extraction against a locally-pulled model served by [Ollama](https://ollama.com), instead of a cloud API — no API key needed, no per-call cost.

```bash
visual-parser --input-dir /path/to/pdfs --vision-provider ollama
```

Omit `--vision-model` and the largest locally-pulled, vision-capable model that fits in currently-free GPU VRAM is auto-selected (logged to the console/`05_pipeline.log` as it's picked). To use a specific model instead, pass it explicitly:

```bash
visual-parser --input-dir /path/to/pdfs --vision-provider ollama --vision-model qwen2.5-vl:32b
```

Auto-selection:
- Pull at least one vision-capable model first: `ollama pull llava` (or any other vision-capable tag).
- Vision capability is detected via Ollama's reported model capabilities, falling back to a name heuristic (`llava`, `vision`, `-vl`, `pixtral`, `moondream`, `minicpm-v`, `bakllava`) on older Ollama versions that don't report it.
- The selection budget is 85% of currently-free VRAM (not total VRAM) — this correctly leaves room for whatever else is already resident (e.g. Nougat's model during the same pipeline run) and for the model's own KV-cache/context overhead, which isn't included in its on-disk size.
- If no CUDA GPU is visible to the process at all — including the case of running in a Docker container without `--gpus all` while Ollama runs on the host with a real GPU — CPU-only Ollama is treated as a legitimate setup: auto-selection falls back to the smallest pulled vision-capable model instead of refusing, printing a clear warning that it's running CPU-only and will be slow. Pass an explicit `--vision-model` to pick a different one.
- If a real GPU *is* visible but no vision-capable model fits the free-VRAM budget, that case stays strict — auto-selection raises an error asking for an explicit `--vision-model`, rather than silently falling back to heavy CPU offload.

Reachability: checks `OLLAMA_BASE_URL` (if set) → `http://localhost:11434` → `http://host.docker.internal:11434` (the containerized case). On Docker Desktop (Windows/macOS) the container reaches a host-installed Ollama automatically; on native Linux Docker Engine, add `--add-host=host.docker.internal:host-gateway` to the `docker run` command, or set `OLLAMA_BASE_URL` directly.

---

## Citation

If you use RADIANT-LLM or the accompanying evaluation materials, please cite the journal article:

```bibtex
@article{ndum2026retrieval,
  title={A retrieval-augmented, domain-intelligent agentic framework for reliable decision support in safety-critical nuclear engineering},
  author={Ndum, Zavier Ndum and Tao, Jian and Ford, John and Yim, Mansung and Liu, Yang},
  journal={Reliability Engineering \& System Safety},
  pages={113057},
  year={2026},
  publisher={Elsevier}
}
```

Journal: *Reliability Engineering & System Safety* (2026), article 113057
Preprint: https://arxiv.org/abs/2604.22755

---

## License

Copyright 2026 Zavier N. Ndum

This project is licensed under the Apache License 2.0, the same license as its parent project, [RADIANT-LLM](https://github.com/SmartLabNuclear/RADIANT_LLM). See the [LICENSE](https://github.com/SmartLabNuclear/RADIANT_LLM/blob/main/LICENSE) file in the RADIANT_LLM repository, or the `LICENSE` file bundled with this package, for the full license text.
