# RADIANT-LLM

<!-- ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) -->
![Python 3.12.10](https://img.shields.io/badge/Python-3.12.10-brightgreen.svg)
<!-- ![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg) -->


RADIANT-LLM (**R**etrieval-augmented **D**omain-intelligent assistant for **A**dvanced **N**uclear **T**echnologies) is a local-first, model-agnostic Visual-RAG (visual retrieval-augmented generation) system for secure, document-grounded assistance in Nuclear Science and Engineering (NSE). It combines multi-modal ingestion (text plus visual context) with a structured knowledge base to enable page- and figure-level retrieval from complex technical documents with auditable, citation-backed responses, while respecting privacy/security constraints by keeping data processing local and emphasizing auditable, citation-traceable outputs.


## Highlights of the Methodology
- Secure, document-grounded Visual-RAG layer for NSE-based knowledge management 
- Multi-modal ingestion with page/figure-aware retrieval and citations.
- Domain-aware evaluation metrics: Context Precision (CoP), Citation Precision (CiP), Citation Hit (CiH), Hallucination Rate (HR), and Visual Recall (ViR).

---

## Highlights of the Results 

### Cross-platform performance on UNFSF Visual-RAG benchmark

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

## Evaluation Materials

The evaluation package in [`radiant-llm-evaluation/`](radiant-llm-evaluation/) includes the supplementary material PDF, benchmark query files, scoring rubrics, expert scoring files, model responses, and statistical plots used to support the reported RADIANT-LLM results.

- Supplementary material: [`radiant-llm-supplementary-material.pdf`](radiant-llm-evaluation/radiant-llm-supplementary-material.pdf)
- Page-level benchmark materials: [`Page_level/`](radiant-llm-evaluation/Page_level/)
- Context-scaling benchmark materials: [`Context_scaling/`](radiant-llm-evaluation/Context_scaling/)
- Final statistical plots: [`final_statistical_analysis/Plots/`](radiant-llm-evaluation/final_statistical_analysis/Plots/)

---

## Standalone PDF ingestion: `visual-parser`

This repo also includes `visual-parser`, a standalone PDF ingestion tool that accelerates document processing by generating JSONL knowledge bases (text chunks + figure descriptions + metadata) from curated PDFs. You can run `visual-parser` first to build a high-fidelity, multi-modal KB, then run RADIANT-LLM Visual-RAG for QA over that KB.

See [`codebase/Visual-Parser/README.md`](codebase/Visual-Parser/README.md) for CLI/Docker usage and model configuration options.

---
## Prerequisites: API keys

You will typically need at least one LLM provider key:
- OpenAI API key: https://platform.openai.com/api-keys
- Gemini API key (AI Studio): https://aistudio.google.com/app/apikey

Optional (depending on enabled tools/features):
- LangChain / LangSmith API key (tracing/logs): https://www.langchain.com/langsmith
- Google Custom Search API key: https://developers.google.com/custom-search/v1/introduction
- Google Custom Search Engine ID: https://programmablesearchengine.google.com/controlpanel/overview

Create a `.env` file with your API keys (for example `OPENAI_API_KEY=...`). Pass it at runtime with `--env-file .env` (path can be anywhere on the host).

---

## Quick Start: Docker (prebuilt images)

Prebuilt images are published on Docker Hub: **[zev94/radiant-llm](https://hub.docker.com/r/zev94/radiant-llm)**.  


| Tag | Application |
|-----|-------------|
| `1.0`, `latest` | **RADIANT-LLM** — chat UI for Visual-RAG over your knowledge base |
| `visual-parser-1.0`, `visual-parser-latest` | **visual-parser** — PDF → JSONL knowledge-base ingestion |

### Prerequisites
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- A `.env` file with at least one LLM provider key (`OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.)
- (Optional, for GPU) NVIDIA GPU + recent drivers + NVIDIA Container Toolkit (`docker run --gpus all`)

### 1) Pull RADIANT-LLM
```bash
docker pull zev94/radiant-llm:1.0
```

Windows PowerShell:
```powershell
docker pull zev94/radiant-llm:1.0
```

### 2) Run RADIANT-LLM
The container serves the web UI on port **8080** inside the image. Map host **8060** → container **8080**.

Mount a **skills** folder (read-only; not baked into the image), an optional **working directory** for PDF/CSV tools, and a **logs** folder so reasoning/streaming logs persist on the host (`RADIANT_LLM_Logs` on the host → `/radiant-llm/RADIANT_LLM_Logs` in the container).

Windows PowerShell:
```powershell
docker run -d --name radiant-llm `
  -p 8060:8080 `
  --env-file .env `
  -v "C:\path\to\radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro" `
  -v "C:\path\to\your\data:/workdir" `
  -v "${PWD}\RADIANT_LLM_Logs:/radiant-llm/RADIANT_LLM_Logs" `
  zev94/radiant-llm:1.0
```

WSL (Ubuntu):
```bash
docker run -d --name radiant-llm \
  -p 8060:8080 \
  --env-file .env \
  -v "/mnt/c/path/to/radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro" \
  -v "/mnt/c/path/to/your/data:/workdir" \
  -v "$PWD/RADIANT_LLM_Logs:/radiant-llm/RADIANT_LLM_Logs" \
  zev94/radiant-llm:1.0
```

Linux:
```bash
docker run -d --name radiant-llm \
  -p 8060:8080 \
  --env-file .env \
  -v "/path/to/radiant_llm_skills:/radiant-llm/radiant_llm_skills:ro" \
  -v "/path/to/your/data:/workdir" \
  -v "$PWD/RADIANT_LLM_Logs:/radiant-llm/RADIANT_LLM_Logs" \
  zev94/radiant-llm:1.0
```

Optional (GPU): add `--gpus all` to `docker run`.

### 3) Open the web GUI
```text
http://localhost:8060
```

Verify / tail logs:
```bash
docker ps
docker logs -f radiant-llm
```

### 4) Set Working Directory in the UI
Use a path **inside the container** under your mounted folder, for example:
```text
/workdir
```

### 5) Pull and run visual-parser (optional)
Build a multi-modal JSONL knowledge base before or alongside RADIANT-LLM QA. See [`visual-parser/README.md`](visual-parser/README.md) for CLI flags.

```bash
docker pull zev94/radiant-llm:visual-parser-1.0
```

Windows PowerShell:
```powershell
docker run --rm --env-file .env `
  -v "C:\path\to\pdfs:/data" `
  zev94/radiant-llm:visual-parser-1.0 `
  --input-dir /data --output-dir /data
```

WSL / Linux:
```bash
docker run --rm --env-file .env \
  -v "/path/to/pdfs:/data" \
  zev94/radiant-llm:visual-parser-1.0 \
  --input-dir /data --output-dir /data
```

Help:
```bash
docker run --rm zev94/radiant-llm:visual-parser-1.0 --help
```

---

### Offline install (legacy `.tar` releases)

If you have a release `.tar` instead of Hub access:

```powershell
docker load -i .\radiant-llm_0.1.0.tar
docker images   # use the tag printed by Docker
```

Older images used port `8050`, mount path `/host_data`, and log folder `DecodedAI_logs`. Current Hub images use `8060:8080`, `/workdir`, and **`RADIANT_LLM_Logs`** → `/radiant-llm/RADIANT_LLM_Logs`.

---

## Troubleshooting

- **pull access denied / repository does not exist**
  - Log in: `docker login`
  - Use the full image name: `zev94/radiant-llm:1.0` (not a local-only name unless you built or loaded it yourself).

- **Invalid directory. Default temporary directory is being used**
  - The UI working-directory path must exist inside the container.
  - Match the right-hand side of your volume mount (for example mount to `/workdir`, then use `/workdir/...` in the UI).

- **Skills not loading**
  - Mount skills at `/radiant-llm/radiant_llm_skills`, or set **Skills directory** in Settings to your custom mount path.

- **GPU not detected**
  - Verify GPU support with: `docker run --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi`

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

This repository is currently proprietary and not licensed for public use, redistribution, or modification. Licensing terms will be updated after institutional review.
