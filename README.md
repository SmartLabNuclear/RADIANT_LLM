
<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/SmartLabNuclear/RADIANT_LLM?style=social)](https://github.com/SmartLabNuclear/RADIANT_LLM/stargazers)
![Python 3.12.10](https://img.shields.io/badge/Python-3.12.10-brightgreen.svg)
[![Built with LangChain](https://img.shields.io/badge/Built%20with-LangChain-1C3C3C.svg)](https://www.langchain.com/)
[![Docker Pulls](https://img.shields.io/docker/pulls/zev94/radiant-llm.svg)](https://hub.docker.com/r/zev94/radiant-llm)
[![Last Commit](https://img.shields.io/github/last-commit/SmartLabNuclear/RADIANT_LLM.svg)](https://github.com/SmartLabNuclear/RADIANT_LLM/commits)

### ⭐ If RADIANT-LLM is useful to you, please consider starring the repo, it genuinely helps others discover the project.

### 💬 Using RADIANT-LLM (or its related tools/papers)? I'd appreciate ~5 minutes of your feedback, it directly shapes what gets prioritized next: [Share your experience](https://forms.gle/bU5th8vfPXdcxbNT9)

</div>

# RADIANT-LLM

<!-- ![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg) -->

<p align="center">
  <a href="./RADIANT_LLM_GUI_2_0.png">
    <img src="./RADIANT_LLM_GUI_2_0.png" alt="RADIANT-LLM interface" width="720">
  </a>
</p>

RADIANT-LLM (**R**etrieval-augmented **D**omain-intelligent assistant for **A**dvanced **N**uclear **T**echnologies) is a local-first, model-agnostic Visual-RAG (visual retrieval-augmented generation) system for secure, document-grounded assistance in Nuclear Science and Engineering (NSE). It combines multi-modal ingestion (text plus visual context) with a structured knowledge base to enable page- and figure-level retrieval from complex technical documents with auditable, citation-backed responses, while respecting privacy/security constraints by keeping data processing local and emphasizing auditable, citation-traceable outputs.

This repository also includes [`Visual-Parser`](Visual-Parser/README.md), a standalone PDF ingestion tool for generating JSONL knowledge bases from curated documents. It is available on PyPI at https://pypi.org/project/visual-parser/ and can be used independently of the RADIANT-LLM chat UI.

## Table of Contents

- [Highlights of the Methodology](#highlights-of-the-methodology)
- [Highlights of the Results](#highlights-of-the-results)
- [LearningCenter](#learningcenter)
- [Evaluation Materials](#evaluation-materials)
- [Standalone PDF Ingestion: visual-parser](#standalone-pdf-ingestion-visual-parser)
- [Part 1: Prerequisites](#part-1-prerequisites)
- [Part 2: Prepare Your Local Directory](#part-2-prepare-your-local-directory)
- [Part 3: Run RADIANT-LLM](#part-3-run-radiant-llm)
  - [Option A: Docker Compose (recommended)](#option-a-docker-compose-recommended)
  - [Option B: Plain `docker run` (legacy)](#option-b-plain-docker-run-legacy)
  - [Verify and Open the UI](#verify-and-open-the-ui)
- [Local Models: Grace HPRC vLLM](#local-models-grace-hprc-vllm-optional)
- [Troubleshooting](#troubleshooting)
- [Related Projects](#related-projects)
- [Citation](#citation)
- [License](#license)

New here? Start with **Part 1** and come back once your API keys are ready.

## Highlights of the Methodology
- Secure, document-grounded Visual-RAG layer for NSE-based knowledge management 
- Multi-modal ingestion with page/figure-aware retrieval and citations.
- Domain-aware evaluation metrics: Context Precision (CoP), Citation Precision (CiP), Citation Hit (CiH), Hallucination Rate (HR), and Visual Recall (ViR).

## Highlights of the Results 

### Cross-platform performance on Used Nuclear Fuel Storage Facility (UNFSF) Visual-RAG benchmark

RADIANT-LLM's Visual-RAG layer, powered by GPT-5 over a local 250-source multi-modal knowledge base constructed with GPT-5.2, achieved the highest overall correctness (CoP = 0.875), perfect visual recall (ViR = 1.000), low hallucination (HR = 0.083), and strong citation performance (CiP = 0.862, CiH = 0.833) on twelve expert-curated UNFSF diagnostic queries. ChatGPT with web access and institutional/frozen GPT-5.2 baselines showed weaker page- and figure-level grounding, with no expert-defined anchor hits (CiH = 0).

<a href="Average_scores_platforms.png"><img src="Average_scores_platforms.png" alt="Cross-platform comparison across UNFSF diagnostic queries" width="650"></a>

### Bridging the visual information gap in scientific PDFs
Baseline Nougat parsing loses diagrams and layout, dropping critical visual semantics from complex NSE pages. RADIANT-LLM's multi-modal parsing strategy recovers the visual topology, labels, and relationships into structured data records, making visual content first-class, retrievable evidence for downstream Visual-RAG.

<a href="Visual_Information_Gap.PNG"><img src="Visual_Information_Gap.PNG" alt="Bridging the visual information gap" width="600"></a>

### Page-level visual grounding and knowledge-base fidelity
Across the 30-query page-level benchmark, RADIANT-LLM powered by GPT-5.2 achieved the strongest consensus performance (CoP = 0.958, ViR = 0.911, HR = 0.032). The same benchmark also shows the importance of knowledge-base construction fidelity: GPT-4o improved substantially when queried against a GPT-5.2-constructed multi-modal KB instead of its own page-level KB. These results show that reliable Visual-RAG depends on both model reasoning and high-fidelity ingestion of schematic, geometric, and figure-level evidence.

<a href="radiant-llm-evaluation/final_statistical_analysis/Plots/figure_page_level_bars.png"><img src="radiant-llm-evaluation/final_statistical_analysis/Plots/figure_page_level_bars.png" alt="Page-level benchmark results and cross-model knowledge-base effect" width="650"></a>

### Sensitivity to context scaling in Visual-RAG

For GPT-5.2 on the UNFSF context-scaling benchmark, performance remained strong as the knowledge base expanded from 1 source (27 pages) to 250 sources (16,141 pages). Across conditions, the higher-is-better metrics stayed in strong bands (CoP: 0.813-0.956, CiP: 0.893-0.964, CiH: 0.900-0.989, ViR: 0.802-0.983), while hallucination remained low (HR: 0.024-0.094). Statistical trend testing found no significant monotonic degradation with corpus size, supporting the use of RADIANT-LLM as a reliable QA assistant with expert oversight.

<a href="radiant-llm-evaluation/final_statistical_analysis/Plots/figure_context_scaling_lines.png"><img src="radiant-llm-evaluation/final_statistical_analysis/Plots/figure_context_scaling_lines.png" alt="Context-scaling benchmark results across knowledge-base sizes" width="650"></a>

---

## LearningCenter

The [`LearningCenter/`](LearningCenter/) folder contains a public-facing tutorial notebook for readers who want a compact introduction to RAG concepts before diving into the full Visual-RAG system.

- Notebook: [`LearningCenter/RAG_Agent_Workshop.ipynb`](LearningCenter/RAG_Agent_Workshop.ipynb)
- Folder guide: [`LearningCenter/README.md`](LearningCenter/README.md)

The notebook uses the repository's own supplementary material PDF as its default document source, so the walkthrough stays tied to the RADIANT-LLM methodology and evaluation context rather than a generic toy example.

If the repository, notebook, or evaluation materials support your work, please cite the RADIANT-LLM paper using the metadata in [`CITATION.cff`](CITATION.cff).

---

## Evaluation Materials
The evaluation package in [`radiant-llm-evaluation/`](radiant-llm-evaluation/) includes the supplementary material PDF, benchmark query files, scoring rubrics, expert scoring files, model responses, and statistical plots used to support the reported RADIANT-LLM results.

- Supplementary material: [`radiant-llm-supplementary-material.pdf`](radiant-llm-evaluation/radiant-llm-supplementary-material.pdf)
- Page-level benchmark materials: [`Page_level/`](radiant-llm-evaluation/Page_level/)
- Context-scaling benchmark materials: [`Context_scaling/`](radiant-llm-evaluation/Context_scaling/)
- Final statistical plots: [`final_statistical_analysis/Plots/`](radiant-llm-evaluation/final_statistical_analysis/Plots/)

---

## Standalone PDF ingestion: `visual-parser`

This repo also includes `visual-parser`, a standalone PDF ingestion tool that accelerates document processing by generating JSONL knowledge bases (text chunks + figure descriptions + metadata) from curated PDFs. You can run `visual-parser` first to build a high-fidelity, multi-modal KB, then run RADIANT-LLM Visual-RAG for QA over that KB.

The standalone `visual-parser` package is included in this repository and is covered by the same Apache License 2.0 used across the codebase. See [`Visual-Parser/README.md`](Visual-Parser/README.md) for package-specific usage details.

---

## Part 1: Prerequisites

### API Keys

You will need the following API keys:

- OpenAI API key (one of OpenAI or Gemini is required, this one needs billing set up): [step-by-step guide](LearningCenter/api-key-guides/openai.md)
- Gemini API key (one of OpenAI or Gemini is required, this one is free): [step-by-step guide](LearningCenter/api-key-guides/gemini.md)
- LangChain (LangSmith) API key (optional, for tracing/logs): [step-by-step guide](LearningCenter/api-key-guides/langsmith.md)
- Hugging Face API key (`HF_API_KEY`, required for document parsing in RAG): [step-by-step guide](LearningCenter/api-key-guides/huggingface.md)
- Tavily API key (optional, for live web search — the recommended web-search provider): [step-by-step guide](LearningCenter/api-key-guides/tavily.md)
- Google Custom Search API key and Search Engine ID (optional legacy fallback for web search; Google closed this API to new customers in 2025 and will shut it down entirely on January 1, 2027 — most new users should skip this and use Tavily instead): [step-by-step guide](LearningCenter/api-key-guides/google-custom-search.md)

### Docker

You will also need [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or [Docker Engine](https://docs.docker.com/engine/install/) (Linux).

(Optional, for GPU) NVIDIA GPU + recent drivers + NVIDIA Container Toolkit (`docker run --gpus all`).

### The RADIANT-LLM Image

Prebuilt images are published on Docker Hub: **[zev94/radiant-llm](https://hub.docker.com/r/zev94/radiant-llm)**. No `.tar` download or access request needed, pull it directly.

**RADIANT-LLM (chat UI for Visual-RAG):**
- `zev94/radiant-llm:2.0` — the original fixed build referenced by the RADIANT-LLM paper. Frozen, kept exactly as first published.
- `zev94/radiant-llm:latest` — the rolling tag, always the newest build.
- `zev94/radiant-llm:YYYY-MM-DD` — planned convention for dated snapshots pushed alongside future `:latest` updates, for pinning to a specific known build. See the [full tag list](https://hub.docker.com/r/zev94/radiant-llm/tags) for available tags.

**visual-parser (standalone PDF ingestion):**
- `zev94/radiant-llm:visual-parser-1.0.2` — pinned release.
- `zev94/radiant-llm:visual-parser-latest` — rolling tag, always the newest build.

Both launch methods in [Part 3](#part-3-run-radiant-llm) pull the image automatically, so you don't need to do this manually, but you can get a head start now if you like:

```bash
docker pull zev94/radiant-llm:latest
```

---

## Part 2: Prepare Your Local Directory

With your API keys ready, set up the folders RADIANT-LLM reads from and writes to, plus your `.env` file. This is a one-time setup. Do it once, before your first run, regardless of which launch method you pick in Part 3.

### Volume Layout

The container uses these logical areas:

| Area | Container path | Mode | Purpose |
|------|----------------|------|---------|
| Skills | `/radiant-llm/radiant_llm_skills` | read-only | Bundled/developer domain skills |
| Logs | `/radiant-llm/RADIANT_LLM_Logs` | read-write | Streaming and reasoning logs |
| Sessions | `/radiant-llm/RADIANT_LLM_Sessions` | read-write | Persistent chat session history |
| Working data | `/host` | read-write | Working directory for PDF/CSV/image tools |

**Security note:** whatever folder you mount to `/host` is the *only* folder the agent can read or write. It can create and browse subfolders inside it freely, but it cannot reach anything outside it, including parent directories or other drives. Pick a folder you're comfortable giving RADIANT-LLM full read/write access to, nothing more.

### Download the Skills Folder

Download [`radiant_llm_skills/`](radiant_llm_skills/) from this repository into your run directory. This ships with the bundled domain skills RADIANT-LLM relies on.

### Create the Logs and Sessions Folders

PowerShell:

```powershell
New-Item -ItemType Directory -Force .\RADIANT_LLM_Logs, .\RADIANT_LLM_Sessions | Out-Null
```

Bash / Linux / macOS / WSL:

```bash
mkdir -p RADIANT_LLM_Logs RADIANT_LLM_Sessions
```

### Choose Your Working Directory

RADIANT-LLM also needs a folder to read and write your PDF/CSV/image files from. This can be **any existing folder on your machine** — you don't need to create a new one just for RADIANT-LLM. You'll point Docker at this folder in Part 3.

### Add Your `.env` File

Create a `.env` file in your run directory and set required API keys/secrets. A key-only template is provided at [`Docker_Executable/.env.example`](Docker_Executable/.env.example) (copy and fill values).

**No space between the `=` and your key values.** Your `.env` file should have the following keys (see the links in [Part 1](#api-keys)):

```
OPENAI_API_KEY=<your_key_value>
GEMINI_API_KEY=<your_key_value>
LANGCHAIN_API_KEY=<your_key_value>
HF_API_KEY=<your_key_value>
TAVILY_API_KEY=<your_key_value>
CUSTOM_SEARCH_ENGINE_API_KEY=<your_key_value>
CUSTOM_SEARCH_ENGINE_ID=<your_key_value>
```

At minimum, provide one of `OPENAI_API_KEY` or `GEMINI_API_KEY`, plus `HF_API_KEY` for document parsing. Everything else is optional.

---

## Part 3: Run RADIANT-LLM

With Parts 1 and 2 done, you're ready to start RADIANT-LLM. Pick one of the two options below. Docker Compose is recommended for almost everyone.

The container serves the web UI on port **8080** internally, mapped to host port **8060**.

### Option A: Docker Compose (recommended)

RADIANT-LLM can be started with a single command using the [`docker-compose.yml`](Docker_Executable/docker-compose.yml) file included in this repo.

```bash
cd Docker_Executable
```

Edit the volume paths in `docker-compose.yml` to match your folders from Part 2, copy `.env.example` to `.env` and fill in your API keys, then:

```bash
docker compose up -d          # start in background
docker compose logs -f        # follow logs
docker compose down           # stop and remove container
docker compose up -d --pull always   # pull latest image + restart
```

To pin a specific build instead of the newest rolling build, change `zev94/radiant-llm:latest` to a specific tag (e.g. `zev94/radiant-llm:2.0`) on the `image:` line — see [Part 1](#the-radiant-llm-image) for the tag scheme.

Persistent data lands in `Docker_Executable/RADIANT_LLM_Logs/` and `Docker_Executable/RADIANT_LLM_Sessions/` on your host.

### Option B: Plain `docker run` (legacy)

<details>
<summary>Docker Compose above is the recommended path. Expand for the equivalent plain <code>docker run</code> syntax.</summary>

Using the folders and `.env` file from Part 2:

Windows PowerShell:
```powershell
docker run -d --name radiant-llm `
  -p 8060:8080 `
  --env-file .env `
  -e RADIANT_LLM_SESSION_DIR=/radiant-llm/RADIANT_LLM_Sessions `
  -v "C:\path\to\radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro" `
  -v "C:\path\to\your\data:/host" `
  -v "${PWD}\RADIANT_LLM_Logs:/radiant-llm/RADIANT_LLM_Logs" `
  -v "${PWD}\RADIANT_LLM_Sessions:/radiant-llm/RADIANT_LLM_Sessions" `
  zev94/radiant-llm:latest
```

WSL (Ubuntu):
```bash
docker run -d --name radiant-llm \
  -p 8060:8080 \
  --env-file .env \
  -e RADIANT_LLM_SESSION_DIR=/radiant-llm/RADIANT_LLM_Sessions \
  -v "/mnt/c/path/to/radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro" \
  -v "/mnt/c/path/to/your/data:/host" \
  -v "$PWD/RADIANT_LLM_Logs:/radiant-llm/RADIANT_LLM_Logs" \
  -v "$PWD/RADIANT_LLM_Sessions:/radiant-llm/RADIANT_LLM_Sessions" \
  zev94/radiant-llm:latest
```

Linux:
```bash
docker run -d --name radiant-llm \
  -p 8060:8080 \
  --env-file .env \
  -e RADIANT_LLM_SESSION_DIR=/radiant-llm/RADIANT_LLM_Sessions \
  -v "/path/to/radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro" \
  -v "/path/to/your/data:/host" \
  -v "$PWD/RADIANT_LLM_Logs:/radiant-llm/RADIANT_LLM_Logs" \
  -v "$PWD/RADIANT_LLM_Sessions:/radiant-llm/RADIANT_LLM_Sessions" \
  zev94/radiant-llm:latest
```

Replace `C:\path\to\...` or `/path/to/...` with the folders you chose in Part 2. Pin a specific tag instead of `:latest` for a known build — see [Part 1](#the-radiant-llm-image). Optional (GPU): add `--gpus all`.

Verify, view logs, stop, and remove:
```bash
docker ps
docker logs -f radiant-llm
docker stop radiant-llm
docker rm radiant-llm
```

</details>

### Verify and Open the UI

Check container:
```bash
docker ps
docker logs -f radiant-llm
```

Open:
```text
http://localhost:8060
```

**Set Working Directory and user_skills in the UI** — use a path **inside the container** under your mounted host folder, for example:
```text
/host
```

If you mounted a larger host data root, set the working directory to a subfolder under `/host`, for example:
```text
/host/project_a
```

If the UI auto-fills the **user_skills** field, keep it on a writable path under `/host` such as `/host/user_skills`. You only need to change that field if you intentionally mounted a different writable skills location.

**Pull and run visual-parser (optional)** — build a multi-modal JSONL knowledge base before or alongside RADIANT-LLM QA. See [`Visual-Parser/README.md`](Visual-Parser/README.md) for CLI flags.

```bash
docker pull zev94/radiant-llm:visual-parser-latest
```

Windows PowerShell:
```powershell
docker run --rm --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-latest `
  --input-dir /data --output-dir /data
```

WSL / Linux:
```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-latest \
  --input-dir /data --output-dir /data
```

Help:
```bash
docker run --rm zev94/radiant-llm:visual-parser-latest --help
```

### Offline install (legacy `.tar` releases)

If you have a release `.tar` instead of Hub access:

```powershell
docker load -i .\radiant-llm_0.1.0.tar
docker images   # use the tag printed by Docker
```

Older images used port `8050`, mount path `/host_data`, and log folder `DecodedAI_logs`. Current Hub images use `8060:8080`, `/host`, and **`RADIANT_LLM_Logs`** to `/radiant-llm/RADIANT_LLM_Logs`.

---

## Local Models: Grace HPRC vLLM (optional)

RADIANT-LLM supports self-hosted inference via [vLLM](https://docs.vllm.ai) on the Texas A&M University (TAMU) Grace High Performance Research Computing (HPRC) cluster (or any compatible Slurm + A100 cluster). When configured, Grace model variants appear alongside cloud models (GPT, Gemini) in the model selector — no cloud API key is needed for inference.

**Available variants:**

| Variant | GPUs | Quantization | Context window |
|---------|------|--------------|----------------|
| Grace Gemma 4 26B-A4B | 1× A100 | FP8 | 16,384 tokens |
| Grace Gemma 4 31B | 1× A100 | FP8 | 16,384 tokens |
| Grace Gemma 4 31B (bf16) | 2× A100 | None (full precision) | 4,096 tokens |

**How it works:** A Slurm job runs vLLM on a Grace GPU compute node. An SSH tunnel on your local machine (or Docker host) forwards requests from RADIANT-LLM to that node. No model weights or GPU compute leave the cluster.

**Setup guide:** [`developer_scripts/README.md`](developer_scripts/README.md) — covers Grace account prerequisites, one-time model download, sbatch job templates, tunnel management scripts, and troubleshooting.

> **Docker users:** The SSH tunnel binds to your host machine. RADIANT-LLM running in Docker reaches it automatically via `host.docker.internal` — the provided `docker-compose.yml` and `.env` in this repo already have this configured.

---

## Troubleshooting

- **pull access denied / repository does not exist**
  - Log in: `docker login`
  - Use the full image name: `zev94/radiant-llm:1.0` (not a local-only name unless you built or loaded it yourself).

- **Invalid directory. Default temporary directory is being used**
  - The UI working-directory path must exist inside the container.
  - Match the right-hand side of your volume mount (for example mount to `/host`, then use `/host/...` in the UI).

- **Skills not loading**
  - Mount skills at `/radiant-llm/radiant_llm_skills`, or set **Skills directory** in Settings to your custom mount path.

- **GPU not detected**
  - Verify GPU support with: `docker run --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi`

---

## Related Projects

RADIANT-LLM is part of a broader ecosystem of domain-specific AI agent frameworks that build on this repo's local-LLM and Visual-RAG foundation:

- **[AutoFLUKA](https://github.com/SmartLabNuclear/AutoFLUKA)** — a domain-intelligent LLM agent framework that automates Monte Carlo radiation-transport workflows in FLUKA, from input authoring through execution, self-healing error recovery, and post-processing. It builds on the same local-model and Visual-RAG core documented here; if you're working with FLUKA simulations, AutoFLUKA layers structured domain skills and simulation execution on top of what RADIANT-LLM provides standalone.

A sibling project in the same ecosystem, AutoSAM, also builds on this foundation but does not yet have a public repository.

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

This repository is licensed under the Apache License 2.0. See [`LICENSE`](LICENSE) for details.
