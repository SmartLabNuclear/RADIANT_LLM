"""
config.py — Central configuration for visual_parser.

All settings are read from environment variables (populated from a .env file
at project root via python-dotenv).  Every field has a sensible default so
the tool works out-of-the-box; the user only *needs* to supply an API key for
the chosen vision model.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

from dotenv import load_dotenv

# Load .env: order = global < CWD < explicit (later overrides earlier)
def _load_env():
    # 1) Global: one .env for all runs (any --input-dir).
    # Prefer the current product name, but keep the legacy directory for compatibility.
    global_env_candidates = [
        Path.home() / ".config" / "visual-parser" / ".env",
        Path.home() / ".config" / "visual-rag" / ".env",
    ]
    for global_env in global_env_candidates:
        if global_env.is_file():
            load_dotenv(global_env)
    # 2) Current working directory
    load_dotenv()
    # 3) Explicit path (Docker /env/.env or VISUAL_PARSER_ENV_FILE)
    env_file = os.environ.get("VISUAL_PARSER_ENV_FILE")
    if env_file and os.path.isfile(env_file):
        load_dotenv(env_file)
_load_env()


# ---------------------------------------------------------------------------
# Text-extraction modes
# ---------------------------------------------------------------------------
TextMode = Literal["nougat", "lightweight"]
"""
nougat      – Facebook Nougat transformer model (best for scanned / complex PDFs)
lightweight – PyMuPDF text layer + PyPDFLoader fallback (fast, digital PDFs)
"""

# ---------------------------------------------------------------------------
# Vision-LLM providers
# ---------------------------------------------------------------------------
VisionProvider = Literal["gpt", "gemini"]


@dataclass
class ParserConfig:
    """
    Single source of truth for every knob in the pipeline.

    Instantiate directly or call :func:`ParserConfig.from_env` to read from
    environment variables / a .env file.
    """

    # --- Paths ---------------------------------------------------------------
    input_dir: str = ""
    """Directory that will be scanned recursively for PDF files."""

    output_dir: str = ""
    """
    Directory where JSONL knowledge bases are written.
    Defaults to *input_dir* when left empty.
    """

    # --- Text extraction -----------------------------------------------------
    text_mode: TextMode = "nougat"
    """Which text-extraction engine to use ('nougat' or 'lightweight')."""

    nougat_model: str = "facebook/nougat-small"
    """HuggingFace model identifier for Nougat."""

    chunk_size: int = 500
    """Target character count per text chunk."""

    chunk_overlap: int = 100
    """Character overlap between adjacent chunks."""

    # --- Vision LLM ----------------------------------------------------------
    vision_provider: VisionProvider = "gpt"
    """Which vision LLM to use for figure descriptions and metadata ('gpt' or 'gemini')."""

    # OpenAI
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    gpt_vision_model: str = "gpt-5.4"
    """Default GPT vision model. Also accepts: gpt-5.5, gpt-5.3-chat-latest, gpt-5.2, gpt-5.1, gpt-5, gpt-4o, gpt-4.1"""

    # GPT-5.x reasoning effort: none | low | medium | high | xhigh
    # Older gpt-5 uses minimal | low | medium | high.
    gpt_reasoning_effort: str = "medium"

    # Google Gemini
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_vision_model: str = "gemini-3-pro-preview"
    """Latest Gemini vision model.  Also accepts: gemini-2.5-flash, gemini-1.5-pro"""

    # --- Vision detail -------------------------------------------------------
    vision_detail: Literal["low", "high", "auto"] = "low"
    """
    Image detail level sent to the vision API.
    'low'  → faster & cheaper (recommended for figure detection at scale).
    'high' → higher fidelity (use for small-text schematics).
    """

    # --- Metadata extraction -------------------------------------------------
    metadata_pages: int = 2
    """Number of front pages to send to the vision LLM for metadata extraction."""

    # --- Parallelism ---------------------------------------------------------
    max_workers: int = 4
    """Thread-pool size for parallel PDF processing."""

    # --- Misc ----------------------------------------------------------------
    rebuild: bool = False
    """If True, reprocess all PDFs even if already recorded in 04_processed_pdfs.txt."""

    skip_text: bool = False
    """
    If True, skip text extraction (Step 1) entirely.
    Use when chunking already completed but the vision steps (figures / metadata)
    failed mid-run (e.g. API credit exhaustion).  All PDFs in input_dir are
    re-queued for vision steps; PDFs already present in 02_visuals_kb.jsonl /
    03_metadata_kb.jsonl are skipped automatically.
    """

    log_level: str = "ERROR"

    # -------------------------------------------------------------------------

    @classmethod
    def from_env(cls) -> "ParserConfig":
        """Construct a ParserConfig reading every setting from environment variables."""
        return cls(
            input_dir            = os.getenv("VISUAL_PARSER_INPUT_DIR", ""),
            output_dir           = os.getenv("VISUAL_PARSER_OUTPUT_DIR", ""),
            text_mode            = os.getenv("VISUAL_PARSER_TEXT_MODE", "nougat"),           # type: ignore[arg-type]
            nougat_model         = os.getenv("VISUAL_PARSER_NOUGAT_MODEL", "facebook/nougat-small"),
            chunk_size           = int(os.getenv("VISUAL_PARSER_CHUNK_SIZE", "500")),
            chunk_overlap        = int(os.getenv("VISUAL_PARSER_CHUNK_OVERLAP", "100")),
            vision_provider      = os.getenv("VISUAL_PARSER_VISION_PROVIDER", "gpt"),        # type: ignore[arg-type]
            openai_api_key       = os.getenv("OPENAI_API_KEY", ""),
            gpt_vision_model     = os.getenv("VISUAL_PARSER_GPT_VISION_MODEL", "gpt-5.4"),
            gpt_reasoning_effort = os.getenv("VISUAL_PARSER_GPT_REASONING_EFFORT", "medium"),
            gemini_api_key       = os.getenv("GEMINI_API_KEY", ""),
            gemini_vision_model  = os.getenv("VISUAL_PARSER_GEMINI_VISION_MODEL", "gemini-3-pro-preview"),
            vision_detail        = os.getenv("VISUAL_PARSER_VISION_DETAIL", "low"),          # type: ignore[arg-type]
            metadata_pages       = int(os.getenv("VISUAL_PARSER_METADATA_PAGES", "2")),
            max_workers          = int(os.getenv("VISUAL_PARSER_MAX_WORKERS", "4")),
            rebuild              = os.getenv("VISUAL_PARSER_REBUILD", "false").lower() == "true",
            skip_text            = os.getenv("VISUAL_PARSER_SKIP_TEXT", "false").lower() == "true",
            log_level            = os.getenv("VISUAL_PARSER_LOG_LEVEL", "ERROR"),
        )

    def effective_output_dir(self) -> str:
        """Return output_dir, falling back to input_dir when not set."""
        return self.output_dir if self.output_dir else self.input_dir

    def validate(self) -> None:
        """Raise ValueError for obviously bad configurations."""
        if not self.input_dir:
            raise ValueError("input_dir must be set.")
        if not Path(self.input_dir).is_dir():
            raise ValueError(f"input_dir does not exist: {self.input_dir!r}")
        if self.text_mode not in ("nougat", "lightweight"):
            raise ValueError(f"text_mode must be 'nougat' or 'lightweight', got {self.text_mode!r}")
        if self.vision_provider not in ("gpt", "gemini"):
            raise ValueError(f"vision_provider must be 'gpt' or 'gemini', got {self.vision_provider!r}")
        if self.vision_provider == "gpt" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set when vision_provider='gpt'.")
        if self.vision_provider == "gemini" and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be set when vision_provider='gemini'.")
