"""
cli_main.py - ASCII-safe CLI entry point for the Visual-RAG PDF Parser.

This module exists to keep Windows console help output stable for the
installed ``visual-parser`` command and ``python -m visual_parser``.
"""

from __future__ import annotations

import argparse
import os
import sys


USAGE_EXAMPLES = """
Examples
--------
# Nougat (default) + GPT-5.4 vision
python visual-parser.py --input-dir ./my_pdfs

# Fast lightweight extraction + Gemini
python visual-parser.py --input-dir ./my_pdfs \\
    --text-mode lightweight \\
    --vision-provider gemini \\
    --vision-model gemini-1.5-pro

# Write outputs to a separate directory
python visual-parser.py --input-dir ./my_pdfs --output-dir ./output_kb

# Force re-parse all PDFs (ignore tracking registry)
python visual-parser.py --input-dir ./my_pdfs --rebuild

# High-detail images for dense schematics
python visual-parser.py --input-dir ./my_pdfs --vision-detail high

# Verbose console logging
python visual-parser.py --input-dir ./my_pdfs --log-level INFO
"""


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="visual-parser",
        description=(
            "Visual-RAG PDF Parser - detects new PDFs, extracts text and "
            "figure descriptions, and writes three JSONL knowledge bases:\n"
            "  01_chunks_kb.jsonl   text chunks\n"
            "  02_visuals_kb.jsonl  visual descriptions\n"
            "  03_metadata_kb.jsonl document metadata"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=USAGE_EXAMPLES,
    )

    io_group = parser.add_argument_group("Paths")
    io_group.add_argument(
        "--input-dir",
        "-i",
        required=True,
        metavar="DIR",
        help="Directory to scan for PDF files (searched recursively).",
    )
    io_group.add_argument(
        "--output-dir",
        "-o",
        default="",
        metavar="DIR",
        help="Directory where JSONL files are written. Defaults to --input-dir.",
    )

    text_group = parser.add_argument_group("Text extraction")
    text_group.add_argument(
        "--text-mode",
        choices=["nougat", "lightweight"],
        default="nougat",
        help=(
            "nougat      - Nougat OCR model (best for scanned/complex PDFs, GPU recommended).\n"
            "lightweight - PyMuPDF text layer + PyPDFLoader fallback (fast, no GPU needed)."
        ),
    )
    text_group.add_argument(
        "--nougat-model",
        default="facebook/nougat-small",
        metavar="MODEL_ID",
        help="HuggingFace model ID for Nougat (default: facebook/nougat-small).",
    )
    text_group.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        metavar="N",
        help="Target characters per text chunk (default: 500).",
    )
    text_group.add_argument(
        "--chunk-overlap",
        type=int,
        default=100,
        metavar="N",
        help="Overlap characters between adjacent chunks (default: 100).",
    )

    vision_group = parser.add_argument_group("Vision LLM (figure descriptions & metadata)")
    vision_group.add_argument(
        "--vision-provider",
        choices=["gpt", "gemini"],
        default="gpt",
        help=(
            "gpt    - OpenAI GPT-5.4  (set OPENAI_API_KEY in .env).\n"
            "gemini - Google Gemini   (set GEMINI_API_KEY in .env)."
        ),
    )
    vision_group.add_argument(
        "--vision-model",
        default=None,
        metavar="MODEL_NAME",
        help=(
            "Vision model name. Omit to use the latest for each provider:\n"
            "  gpt    -> gpt-5.4            (also: gpt-5.5, gpt-5.3-chat-latest, gpt-5.2, gpt-5.1, gpt-5, gpt-4o, gpt-4.1)\n"
            "  gemini -> gemini-3-pro-preview (also: gemini-2.5-flash, gemini-1.5-pro)"
        ),
    )
    vision_group.add_argument(
        "--vision-detail",
        choices=["low", "high", "auto"],
        default="low",
        help=(
            "Image detail level (GPT only).\n"
            "low  - faster/cheaper (default, recommended for most use cases).\n"
            "high - better for dense schematics with small text."
        ),
    )
    vision_group.add_argument(
        "--reasoning-effort",
        choices=["minimal", "none", "low", "medium", "high", "xhigh"],
        default="medium",
        help=(
            "Reasoning effort for GPT-5.x models (ignored for Gemini and older GPT).\n"
            "  minimal/none - minimum reasoning, depending on model.\n"
            "  low    - light reasoning.\n"
            "  medium - balanced (default).\n"
            "  high   - deeper reasoning, slower.\n"
            "  xhigh  - maximum depth (gpt-5.2, gpt-5.4, and gpt-5.5)."
        ),
    )
    vision_group.add_argument(
        "--metadata-pages",
        type=int,
        default=2,
        metavar="N",
        help="Number of front pages sent to the vision LLM for metadata extraction (default: 2).",
    )

    perf_group = parser.add_argument_group("Performance")
    perf_group.add_argument(
        "--max-workers",
        type=int,
        default=4,
        metavar="N",
        help="Thread-pool size for parallel PDF processing (default: 4).",
    )

    misc_group = parser.add_argument_group("Miscellaneous")
    misc_group.add_argument(
        "--rebuild",
        action="store_true",
        help=(
            "Reprocess ALL PDFs, ignoring the 04_processed_pdfs.txt registry. "
            "Use after changing prompts, chunking strategy, or switching models."
        ),
    )
    misc_group.add_argument(
        "--skip-text",
        action="store_true",
        help=(
            "Skip text extraction (Step 1) and resume only the vision steps "
            "(figure descriptions + metadata). Use when chunking already completed "
            "but the run was interrupted mid-vision (e.g. API credit exhaustion). "
            "PDFs already present in 02_visuals_kb.jsonl / 03_metadata_kb.jsonl "
            "are skipped automatically — no duplicates."
        ),
    )
    misc_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="ERROR",
        help="Verbosity level written to 05_pipeline.log (default: ERROR).",
    )

    return parser


def main(argv=None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.vision_model is None:
        args.vision_model = (
            "gpt-5.4" if args.vision_provider == "gpt" else "gemini-3-pro-preview"
        )

    from visual_parser.config import ParserConfig

    config = ParserConfig(
        input_dir=os.path.abspath(args.input_dir),
        output_dir=os.path.abspath(args.output_dir) if args.output_dir else "",
        text_mode=args.text_mode,
        nougat_model=args.nougat_model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        vision_provider=args.vision_provider,
        gpt_vision_model=args.vision_model if args.vision_provider == "gpt" else "gpt-5.4",
        gemini_vision_model=(
            args.vision_model if args.vision_provider == "gemini" else "gemini-3-pro-preview"
        ),
        gpt_reasoning_effort=args.reasoning_effort,
        vision_detail=args.vision_detail,
        metadata_pages=args.metadata_pages,
        max_workers=args.max_workers,
        rebuild=args.rebuild,
        skip_text=args.skip_text,
        log_level=args.log_level,
    )

    try:
        config.validate()
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    from visual_parser.pipeline import run_pipeline

    summary = run_pipeline(config)
    if summary.get("failed_basenames"):
        return 2
    return 0
