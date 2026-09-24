# visual-parser (Standalone Visual-RAG PDF Ingestion)

[Python 3.12.10](https://img.shields.io/badge/Python-3.12.10-brightgreen.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1%2B-ee4c2c.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-1C3C3C.svg)
![CUDA](https://img.shields.io/badge/CUDA-optional-76B900.svg)

`visual-parser` is a standalone document-ingestion tool that converts PDFs into a multi-modal JSONL knowledge base (text chunks + figure descriptions + metadata). It was originally extracted from [RADIANT-LLM](https://github.com/SmartLabNuclear/RADIANT_LLM) — born out of the need for a fast, standalone PDF-ingestion path independent of any chatbot. The intended workflow is:

1) Run `visual-parser` on curated PDFs to generate JSONL KB files.
2) Point any downstream RAG system at the generated KB for QA over it — RADIANT-LLM, AutoSAM, and AutoFLUKA all consume the identical JSONL/registry format, so the same generated KB works with any of them without re-parsing.

## Install via pip

```bash
pip install visual-parser
```

Then run it directly against a folder of PDFs:

```bash
visual-parser --input-dir /path/to/pdfs --output-dir /path/to/pdfs
```

See [Common configuration flags](#common-configuration-flags) below for the full flag list, or [Run with Docker](#run-with-docker-docker-hub) if you'd rather not manage a local Python environment. `pip install` doesn't get you GPU acceleration by default — see [GPU support](#gpu-support) below.

## Outputs (JSONL KB)

By default, the pipeline writes:
- `01_chunks_kb.jsonl`: chunked text extracted from PDFs (Nougat by default).
- `02_visuals_kb.jsonl`: figure/page visual descriptions (Vision LLM).
- `03_metadata_kb.jsonl`: document metadata rows (title/author/etc.).
- `04_processed_pdfs.txt`: a tracker so re-runs only process new PDFs (unless `--rebuild`).

## GPU support

`--text-mode nougat` (the default) auto-detects and uses a CUDA GPU when one is available (`torch.cuda.is_available()`) — no flags or code changes needed. **The catch:** a plain `pip install visual-parser` (or `pip install torch`) resolves to PyPI's default **CPU-only** torch wheel, even on a machine with a real GPU. To actually get GPU acceleration, install the matching CUDA build from PyTorch's own index instead, e.g.:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu130
```

Use `cu130` or newer, not `cu126` — `cu126`'s compiled kernels only cover compute capability up to `sm_90` (Hopper); a newer GPU (e.g. Blackwell, `sm_120`) will show `torch.cuda.is_available() == True` but fail on the first real kernel launch. `cu130` covers Blackwell and every older architecture `cu126` did (confirmed live on both an older GPU and a Blackwell laptop this session); it requires an r580+ NVIDIA driver on the host either way. Pick the exact tag matching your driver at [pytorch.org/get-started](https://pytorch.org/get-started/locally/) if `cu130` doesn't apply. Installing `visual-parser` again afterward won't silently downgrade this back to CPU, since the exact version you already have satisfies its own dependency requirement. Verify with:

```bash
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
```

## API keys (`.env`)

Provide at least one provider:
- `OPENAI_API_KEY` (OpenAI)
- `GEMINI_API_KEY` (Gemini)

Optional:
- `HF_TOKEN` (if you use gated Hugging Face models)
- `PORTKEY_API_KEY` + `PORTKEY_OPENAI_PROVIDER_SLUG` — routes OpenAI-family calls (vision LLM + `--list-models`) through a [Portkey](https://portkey.ai) gateway instead of OpenAI directly, exposing whatever models your Portkey account has access to. Only takes effect when `OPENAI_API_KEY` is absent/empty — direct OpenAI always wins when both are set. Set `VISUAL_PARSER_FORCE_PORTKEY=true` to force Portkey even when `OPENAI_API_KEY` is also present (e.g. set at the OS/system level, where commenting it out of `.env` alone can't disable it).

## Run with Docker (Docker Hub)

Prebuilt images are on **[zev94/radiant-llm](https://hub.docker.com/r/zev94/radiant-llm)** under the **visual-parser** tags:

| Tag | Description |
|-----|-------------|
| `visual-parser-latest` | Always latest build (rolling) |
| `visual-parser-2.0.0` | Pinned release (Apache 2.0 release) |
| `visual-parser-1.0` | Legacy — v1.0.0, stale |

### 1) Install Docker
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)

### 2) Pull the image
```bash
docker pull zev94/radiant-llm:visual-parser-latest
```

### 3) Run (input + output on the same mounted folder)
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

### 4) Run (separate output directory)
Windows PowerShell:
```powershell
docker run --rm --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  -v "C:\path\to\out:/out" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /out
```

### GPU acceleration (Docker)

Add `--gpus all` to any of the run commands above to use an NVIDIA GPU for `--text-mode nougat` (the default) instead of CPU — confirmed working out of the box with Docker Desktop's WSL2 backend, no extra host setup needed on most machines. Omit it (or run on a machine with no GPU) and it falls back to CPU automatically:

```powershell
docker run --rm --gpus all --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data
```

### Offline install (legacy `.tar`)

```powershell
docker load -i .\visual-parser_0.1.0.tar
docker images   # use the tag printed by Docker
```

### Model overrides (optional)

Default vision model is **GPT-5.4** when using `--vision-provider gpt`. Override on the command line:

```powershell
docker run --rm --env-file .env -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data --vision-model gpt-5.4
```

<!-- ## Run from source (Python)

From `codebase/Visual-Parser/`:
```powershell
python visual-parser.py --input-dir "C:\path\to\pdfs"
``` -->

## Common configuration flags

After pulling the image, run:

```bash
docker run --rm zev94/radiant-llm:visual-parser-latest --help
```

For copy-paste **Docker** examples (vision presets, text modes, workers, rebuild), see [`docker-usage-examples.md`](docker-usage-examples.md).

Paths:
- `--input-dir` / `-i` (required)
- `--output-dir` / `-o` (default: same as input)

Text extraction:
- `--text-mode nougat|lightweight` (default: `nougat`)
- `--nougat-model facebook/nougat-small`
- `--chunk-size 500`
- `--chunk-overlap 100`

Vision LLM:
- `--vision-provider gpt|gemini` (default: `gpt`)
- `--vision-model gpt-5.2` (or `gpt-4o`, `gemini-2.5-flash`, etc.)
- `--vision-detail low|high|auto`
- `--reasoning-effort none|low|medium|high|xhigh`
- `--metadata-pages 2`

Performance / misc:
- `--max-workers 4`
- `--rebuild` (reprocess everything; ignore `04_processed_pdfs.txt`)
- `--list-models` — print the live, currently-available vision models for whichever provider(s) you have a key configured for, then exit (no PDF processing). Reflects Portkey's catalog too when that's what's active.
- `--version` / `-V`
- `--log-level DEBUG|INFO|WARNING|ERROR`

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


