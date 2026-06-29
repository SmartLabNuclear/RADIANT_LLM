"""
pipeline.py — The main Visual-RAG parsing orchestrator.

Calls each stage in order:
    0.   Detect new PDFs
    0.5  Extract per-document metadata (Vision LLM on front pages)
    1.   Extract and chunk text  (Nougat  OR  Lightweight, controlled by config)
    2.   Describe figures        (Vision LLM, page-by-page)
    3.   Write metadata JSONL
    4.   Mark PDFs as processed

No vector store, no embeddings, no retrieval — pure JSONL generation.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from visual_parser.config import ParserConfig
from visual_parser.figure_describer import describe_figures_for_new_pdfs
from visual_parser.jsonl_writer import append_to_jsonl, make_document_id
from visual_parser.metadata_extractor import extract_pdf_metadata
from visual_parser.pdf_tracker import (
    PROCESSED_REGISTRY,
    find_new_pdfs,
    mark_as_processed,
)

logger = logging.getLogger(__name__)


def _setup_logging(config: ParserConfig) -> None:
    log_level = getattr(logging, config.log_level.upper(), logging.ERROR)
    log_path  = os.path.join(config.effective_output_dir(), "05_pipeline.log")
    logging.basicConfig(
        filename=log_path,
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    # Also log to stdout so the CLI shows progress
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logging.getLogger().addHandler(console)


def run_pipeline(config: Optional[ParserConfig] = None) -> Dict:
    """
    Execute the full Visual-RAG parsing pipeline.

    Args:
        config: A :class:`~visual_parser.config.ParserConfig` instance.
                When *None*, one is built from environment variables via
                :meth:`ParserConfig.from_env`.

    Returns:
        A summary dict::

            {
                "new_pdfs_found":       int,
                "text_chunks_written":  int,
                "figures_written":      int,
                "metadata_written":     int,
                "processed_basenames":  List[str],
            }
    """
    if config is None:
        config = ParserConfig.from_env()

    config.validate()
    output_dir = config.effective_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    _setup_logging(config)

    summary = {
        "new_pdfs_found":      0,
        "text_chunks_written": 0,
        "figures_written":     0,
        "metadata_written":    0,
        "processed_basenames": [],
        "failed_basenames":    [],
        "status":              "success",
    }

    # -----------------------------------------------------------------------
    # Step 0 — Discover PDFs to process
    # -----------------------------------------------------------------------
    registry_path = os.path.join(output_dir, PROCESSED_REGISTRY)

    _vision_api_key = (
        config.openai_api_key if config.vision_provider == "gpt" else config.gemini_api_key
    )
    _vision_model = (
        config.gpt_vision_model if config.vision_provider == "gpt" else config.gemini_vision_model
    )

    if config.skip_text:
        # --skip-text mode: text extraction already done externally.
        # Use ALL PDFs in input_dir regardless of the tracker; vision steps
        # perform their own deduplication against existing JSONL files.
        import json as _json

        all_pdfs = sorted([
            os.path.join(root, f)
            for root, _, files in os.walk(config.input_dir)
            for f in files
            if f.lower().endswith(".pdf")
        ])

        if not all_pdfs:
            print("No PDFs found in input directory. Nothing to do.")
            return summary

        # Build set of PDFs already in 03_metadata_kb.jsonl (PDF-level, skip whole PDF)
        # 02_visuals_kb.jsonl deduplication is handled at page level inside
        # figure_describer.py — all PDFs are passed so partial PDFs can resume.
        def _sources_in_jsonl(path: str) -> set:
            if not os.path.exists(path):
                return set()
            sources = set()
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        sources.add(_json.loads(line).get("source", ""))
                    except Exception:
                        pass
            return sources

        already_metaed = _sources_in_jsonl(os.path.join(output_dir, "03_metadata_kb.jsonl"))
        pdfs_for_meta  = [p for p in all_pdfs if os.path.basename(p) not in already_metaed]

        print(f"--skip-text mode: {len(all_pdfs)} PDF(s) in directory.")
        print(f"  Already in 03_metadata_kb.jsonl : {len(already_metaed)}")
        print(f"  Remaining for metadata           : {len(pdfs_for_meta)}")
        print(f"  Figures: page-level resume handled automatically.")
        print()

        summary["new_pdfs_found"] = len(all_pdfs)

        # Step 0.5 — Metadata (only for PDFs not yet in 03_metadata_kb.jsonl)
        pdf_meta_map: Dict[str, dict] = {}
        if pdfs_for_meta:
            print(f"[Step 0.5] Extracting metadata for {len(pdfs_for_meta)} PDF(s) …")
            for pdf_path in pdfs_for_meta:
                try:
                    meta = extract_pdf_metadata(
                        pdf_path         = pdf_path,
                        vision_provider  = config.vision_provider,
                        vision_api_key   = _vision_api_key,
                        vision_model     = _vision_model,
                        num_pages        = config.metadata_pages,
                        vision_detail    = config.vision_detail,
                        reasoning_effort = config.gpt_reasoning_effort,
                    )
                    pdf_meta_map[pdf_path] = meta
                except Exception as exc:
                    logger.warning("Metadata extraction failed for %s: %s", pdf_path, exc)
                    pdf_meta_map[pdf_path] = {"_error": str(exc)}
        else:
            print("[Step 0.5] All PDFs already have metadata records — skipping.")

        # Step 1 — Skipped
        print("[Step 1] Skipped (--skip-text).")
        processed_basenames = [os.path.basename(p) for p in all_pdfs]
        failed_basenames: List[str] = []
        summary["processed_basenames"] = processed_basenames
        summary["text_chunks_written"] = 0

        # Step 2 — Figure description
        figures_path   = os.path.join(output_dir, "02_visuals_kb.jsonl")
        figures_before = sum(
            1 for line in open(figures_path, encoding="utf-8") if line.strip()
        ) if os.path.exists(figures_path) else 0

        print(f"[Step 2] Describing figures for {len(all_pdfs)} PDF(s) (page-level resume active) …")
        describe_figures_for_new_pdfs(
            new_pdf_paths    = all_pdfs,
            output_dir       = output_dir,
            vision_provider  = config.vision_provider,
            vision_api_key   = _vision_api_key,
            vision_model     = _vision_model,
            vision_detail    = config.vision_detail,
            reasoning_effort = config.gpt_reasoning_effort,
        )
        figures_after = sum(
            1 for line in open(figures_path, encoding="utf-8") if line.strip()
        ) if os.path.exists(figures_path) else 0
        summary["figures_written"] = max(0, figures_after - figures_before)

        # Step 3 — Metadata JSONL
        print("[Step 3] Writing document metadata …")
        metadata_rows: List[dict] = []
        for pdf_path, meta in pdf_meta_map.items():
            source      = os.path.basename(pdf_path)
            document_id = make_document_id(source)
            row         = {"source": source, "document_id": document_id}
            if isinstance(meta, dict):
                row.update(meta)
            metadata_rows.append(row)

        if metadata_rows:
            metadata_path = os.path.join(output_dir, "03_metadata_kb.jsonl")
            append_to_jsonl(metadata_path, metadata_rows)
            summary["metadata_written"] = len(metadata_rows)
            print(f"[Step 3] Wrote {len(metadata_rows)} metadata record(s).")

        # Step 4 — Mark all PDFs as processed
        print("[Step 4] Updating processed-PDFs registry …")
        mark_as_processed(registry_path, processed_basenames)

    else:
        # ── Normal (full) pipeline ───────────────────────────────────────────

        new_pdfs = find_new_pdfs(config.input_dir, rebuild=config.rebuild)
        summary["new_pdfs_found"] = len(new_pdfs)

        if not new_pdfs:
            print("No new PDFs found. Nothing to do.")
            return summary

        print(f"Found {len(new_pdfs)} new PDF(s). Starting pipeline …")

        # Step 0.5 — Metadata extraction
        pdf_meta_map = {}
        for pdf_path in new_pdfs:
            try:
                meta = extract_pdf_metadata(
                    pdf_path         = pdf_path,
                    vision_provider  = config.vision_provider,
                    vision_api_key   = _vision_api_key,
                    vision_model     = _vision_model,
                    num_pages        = config.metadata_pages,
                    vision_detail    = config.vision_detail,
                    reasoning_effort = config.gpt_reasoning_effort,
                )
                pdf_meta_map[pdf_path] = meta
            except Exception as exc:
                logger.warning("Metadata extraction failed for %s: %s", pdf_path, exc)
                pdf_meta_map[pdf_path] = {"_error": str(exc)}

        # Step 1 — Text extraction and chunking
        if config.text_mode == "nougat":
            print("[Step 1] Running Nougat text extraction …")
            from visual_parser.nougat_engine import NougatInitializer
            from visual_parser.text_extractor import nougat_extract_pdfs

            processor, model, device = NougatInitializer(config.nougat_model)
            nougat_summary, processed_basenames, failed_basenames, chunk_count = nougat_extract_pdfs(
                only_process_these = new_pdfs,
                output_dir         = output_dir,
                processor          = processor,
                model              = model,
                device             = device,
                chunk_size         = config.chunk_size,
                chunk_overlap      = config.chunk_overlap,
                max_workers        = config.max_workers,
            )
            print(nougat_summary)

        else:  # "lightweight"
            print("[Step 1] Running lightweight (PyMuPDF) text extraction …")
            from visual_parser.text_extractor import lightweight_extract_pdfs

            lw_summary, processed_basenames, failed_basenames, chunk_count = lightweight_extract_pdfs(
                only_process_these = new_pdfs,
                output_dir         = output_dir,
                chunk_size         = config.chunk_size,
                chunk_overlap      = config.chunk_overlap,
                max_workers        = config.max_workers,
            )
            print(lw_summary)

        summary["processed_basenames"] = processed_basenames
        summary["failed_basenames"]    = failed_basenames
        summary["text_chunks_written"] = chunk_count

        # Step 2 — Figure description
        figures_path = os.path.join(output_dir, "02_visuals_kb.jsonl")

        def _count_lines(path: str) -> int:
            if not os.path.exists(path):
                return 0
            with open(path, encoding="utf-8") as fh:
                return sum(1 for line in fh if line.strip())

        figures_before = _count_lines(figures_path)

        pdfs_for_figures = [
            p for p in new_pdfs
            if os.path.basename(p) in processed_basenames
        ]

        if pdfs_for_figures:
            print(f"[Step 2] Describing figures in {len(pdfs_for_figures)} PDF(s) …")
            describe_figures_for_new_pdfs(
                new_pdf_paths    = pdfs_for_figures,
                output_dir       = output_dir,
                vision_provider  = config.vision_provider,
                vision_api_key   = _vision_api_key,
                vision_model     = _vision_model,
                vision_detail    = config.vision_detail,
                reasoning_effort = config.gpt_reasoning_effort,
            )
            summary["figures_written"] = max(0, _count_lines(figures_path) - figures_before)
        else:
            print("[Step 2] No PDFs were successfully text-extracted; skipping figure description.")

        # Step 3 — Write metadata JSONL
        print("[Step 3] Writing document metadata …")
        processed_set  = set(processed_basenames)
        metadata_rows = []
        for pdf_path, meta in pdf_meta_map.items():
            source = os.path.basename(pdf_path)
            if source not in processed_set:
                logger.warning("Skipping metadata for %s (text extraction failed).", source)
                continue
            document_id = make_document_id(source)
            row         = {"source": source, "document_id": document_id}
            if isinstance(meta, dict):
                row.update(meta)
            metadata_rows.append(row)

        if metadata_rows:
            metadata_path = os.path.join(output_dir, "03_metadata_kb.jsonl")
            append_to_jsonl(metadata_path, metadata_rows)
            summary["metadata_written"] = len(metadata_rows)
            print(f"[Step 3] Wrote {len(metadata_rows)} metadata record(s).")

        # Step 4 — Persist the processing registry
        print("[Step 4] Updating processed-PDFs registry …")
        mark_as_processed(registry_path, processed_basenames)

    # -----------------------------------------------------------------------
    # Final summary
    # -----------------------------------------------------------------------
    if summary["failed_basenames"] and summary["processed_basenames"]:
        summary["status"] = "partial_failure"
    elif summary["failed_basenames"]:
        summary["status"] = "failed"
    
    print("\n" + "=" * 60)
    if summary["status"] == "success":
        print("Visual-Parser Pipeline Complete")
    elif summary["status"] == "partial_failure":
        print("Visual-Parser Pipeline Completed with Errors")
    else:
        print("Visual-Parser Pipeline Failed")
    print(f"  Total PDFs processed  : {len(processed_basenames)}")
    print(f"  Total PDFs failed     : {len(failed_basenames)}")
    print(f"  Total Text chunks     : {summary['text_chunks_written']}")
    print(f"  Total Figure records  : {summary['figures_written']}")
    print(f"  Total Metadata records: {summary['metadata_written']}")
    print(f"  Output directory: {output_dir}")
    if failed_basenames:
        print(f"  Failed PDFs           : {', '.join(failed_basenames)}")
    print("=" * 60)

    return summary
