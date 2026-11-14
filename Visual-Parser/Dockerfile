# ============================================================
# visual-parser Dockerfile
# ============================================================
# Build:  docker build -t zev94/radiant-llm:visual-parser-2.2.5 .
#
# Built from a clean Python base. Earlier images started FROM an old
# working image that already held PyMuPDF/MuPDF (AGPL) and Levenshtein (GPL);
# files in a base layer ship even if a later layer uninstalls them, so this
# image starts from python:3.11-slim and installs only what Visual-Parser needs.
#
# Nougat model is downloaded during build so runs start without re-downloading.
# (Do not pass secrets via ARG/ENV; they can leak into image history.)
# One .env in a single place; point --input-dir to any PDF directory.
# No need for .env inside every folder you run on.
# ============================================================

FROM python:3.11-slim

WORKDIR /app

# tesseract-ocr: optional equation OCR for the lightweight text engine (pytesseract).
# The old base image also installed libmupdf-dev (MuPDF, AGPL) -- deliberately not here.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Torch first, from the CUDA index, in this one layer (so the CPU wheels are never
# installed and then overwritten, which would leave both copies in the image).
#
# cu130 (not cu126): PyTorch's compiled kernels are architecture-specific --
# cu126 only ships kernels through sm_90 (Hopper), so torch.cuda.is_available()
# returns True on a newer GPU (e.g. Blackwell, sm_120) but the first real
# kernel launch fails since there's no compiled/PTX code for that arch. cu130
# covers sm_120 and every older arch cu126 supported, so this one build works
# across GPU generations. Requires an r580+ NVIDIA driver on the host either way.
# Falls back to CPU cleanly either way via NougatInitializer's own
# torch.cuda.is_available() check -- no code change needed for that part.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu130

# Visual-Parser and its dependencies (pyproject.toml; [ocr] adds pytesseract).
# pyproject.toml is only needed at build time; not kept in the final image.
COPY pyproject.toml README.md LICENSE ./
COPY visual_parser ./visual_parser
# Windows editors often save UTF-8 BOM; tomllib rejects it at byte 0.
RUN python -c "p=open('pyproject.toml','rb').read(); open('pyproject.toml','wb').write(p.lstrip(b'\xef\xbb\xbf'))" \
    && pip install --no-cache-dir ".[ocr]" \
    && rm -rf pyproject.toml README.md LICENSE visual_parser

# Pre-download Nougat model at build time (so runs start without re-downloading)
RUN python -c "from visual_parser.nougat_engine import NougatInitializer; NougatInitializer()"

# --------------------------------------------
# Runtime: API keys via --env-file or /env mount
# --------------------------------------------
# Option A (recommended, like AutoFLUKA): pass your .env file once per run
#   docker run --rm --env-file .env -v C:\path\to\pdfs:/data visual-parser --input-dir /data --output-dir /data
#   Use any PDF directory; .env can live in the current dir or any path: --env-file C:\config\.env
#
# GPU acceleration (--text-mode nougat, the default): add --gpus all if the host
# has an NVIDIA GPU + driver (Docker Desktop's WSL2 backend passes it through
# with no extra setup on most machines; confirmed via `docker run --gpus all
# nvidia/cuda:... nvidia-smi`). Falls back to CPU automatically if omitted or
# if no GPU is present -- same command works either way:
#   docker run --rm --gpus all --env-file .env -v C:\path\to\pdfs:/data visual-parser --input-dir /data --output-dir /data
#
# Option B: mount a config dir at /env (app loads /env/.env automatically)
#   docker run --rm -v C:\visual-parser-config:/env -v C:\thesis\chapter2:/data visual-parser:1.0.0 --input-dir /data --output-dir /data
#
# .env should contain OPENAI_API_KEY and/or GEMINI_API_KEY, optional HF_TOKEN.
#
# --vision-provider ollama (local, no API key): the container reaches a
# host-installed Ollama via http://host.docker.internal:11434 by default.
# On Docker Desktop (Windows/macOS) this resolves automatically -- no change
# needed. On native Linux Docker Engine, add --add-host to the run command:
#   docker run --rm --add-host=host.docker.internal:host-gateway --gpus all \
#     --env-file .env -v C:\path\to\pdfs:/data visual-parser \
#     --input-dir /data --output-dir /data --vision-provider ollama
# Or set OLLAMA_BASE_URL directly in .env to skip autodetection entirely.
# --------------------------------------------
# Unbuffered output so progress appears in the terminal as it runs (not only at the end)
ENV PYTHONUNBUFFERED=1

ENV IN_DOCKER="1"
ENV VISUAL_PARSER_ENV_FILE="/env/.env"

VOLUME ["/env", "/data"]

ENTRYPOINT ["python", "-u", "-m", "visual_parser"]
CMD ["--help"]
