# visual-parser (Standalone Visual-RAG PDF Ingestion)

![Python 3.12.10](https://img.shields.io/badge/Python-3.12.10-brightgreen.svg)
<!-- ![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg) -->

`visual-parser` is a standalone document-ingestion tool that converts PDFs into a multi-modal JSONL knowledge base (text chunks + figure descriptions + metadata). The intended workflow is:

1) Run `visual-parser` on curated PDFs to generate JSONL KB files.
2) Run RADIANT-LLM Visual-RAG for QA over the generated KB.

## Outputs (JSONL KB)

By default, the pipeline writes:
- `01_chunks_kb.jsonl`: chunked text extracted from PDFs (Nougat by default).
- `02_visuals_kb.jsonl`: figure/page visual descriptions (Vision LLM).
- `03_metadata_kb.jsonl`: document metadata rows (title/author/etc.).
- `04_processed_pdfs.txt`: a tracker so re-runs only process new PDFs (unless `--rebuild`).

## API keys (`.env`)

Provide at least one provider:
- `OPENAI_API_KEY` (OpenAI)
- `GEMINI_API_KEY` (Gemini)

Optional:
- `HF_TOKEN` (if you use gated Hugging Face models)

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

### Offline install (legacy `.tar`)

```powershell
docker load -i .\visual-parser_0.1.0.tar
docker images   # use the tag printed by Docker
```

### Model overrides (optional)

Default vision model is **GPT-5.5** when using `--vision-provider gpt`. Override on the command line:

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
- `--log-level DEBUG|INFO|WARNING|ERROR`

---

## Citation

If you use RADIANT-LLM or the accompanying evaluation materials, please cite the preprint:

```bibtex
@article{ndum2026radiant,
  title={RADIANT-LLM: an Agentic Retrieval Augmented Generation Framework for Reliable Decision Support in Safety-Critical Nuclear Engineering},
  author={Ndum, Zavier Ndum and Tao, Jian and Ford, John and Yim, Mansung and Liu, Yang},
  journal={arXiv preprint arXiv:2604.22755},
  year={2026}
}
```

Preprint: https://arxiv.org/abs/2604.22755

---

## License

This project is licensed under the Apache License 2.0. See the top-level [`LICENSE`](../LICENSE) for the full license text.


