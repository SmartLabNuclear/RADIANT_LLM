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
from visual_parser.jsonl_writer import append_to_jsonl, make_document_id, read_jsonl
from visual_parser.metadata_extractor import extract_pdf_metadata
from visual_parser.pdf_tracker import (
    PROCESSED_REGISTRY,
    find_new_pdfs,
    load_processed_pdfs,
    mark_as_processed,
    save_processed_pdfs,
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


def _recover_stale_registry_entries(input_dir: str, output_dir: str, registry_path: str) -> int:
    """
    Remove processed-PDF registry entries for files that have no chunk records.
    This recovers from earlier failed runs that incorrectly marked PDFs as done.
    """
    if not os.path.exists(registry_path):
        return 0

    processed = load_processed_pdfs(registry_path)
    if not processed:
        return 0

    existing_basenames = {
        filename.lower()
        for root, _, files in os.walk(input_dir)
        for filename in files
        if filename.lower().endswith(".pdf")
    }
    if not existing_basenames:
        return 0

    chunks_path = os.path.join(output_dir, "01_chunks_kb.jsonl")
    visuals_path = os.path.join(output_dir, "02_visuals_kb.jsonl")
    extracted_sources = set()

    for row in read_jsonl(chunks_path):
        source = row.get("source")
        if isinstance(source, str) and source.lower().endswith(".pdf"):
            extracted_sources.add(source.lower())

    for row in read_jsonl(visuals_path):
        source = row.get("source")
        if isinstance(source, str) and source.lower().endswith(".pdf"):
            extracted_sources.add(source.lower())

    stale = [
        name for name in processed
        if name.lower() in existing_basenames and name.lower() not in extracted_sources
    ]
    if not stale:
        return 0

    cleaned = [name for name in processed if name not in stale]
    save_processed_pdfs(registry_path, sorted(set(cleaned)))
    logger.warning(
        "Recovered %d stale processed registry entries: %s",
        len(stale),
        ", ".join(sorted(stale)),
    )
    return len(stale)


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

    if config.vision_provider == "gpt":
        _vision_api_key = config.openai_api_key
        _vision_model = config.gpt_vision_model
    elif config.vision_provider == "gemini":
        _vision_api_key = config.gemini_api_key
        _vision_model = config.gemini_vision_model
    else:  # "ollama" -- no API key needed
        _vision_api_key = ""
        _vision_model = None  # resolved lazily by _ensure_ollama_vision_model()

    _ollama_resolved = False

    def _ensure_ollama_vision_model() -> None:
        # Deliberately lazy: resolving a name (possibly a network call to
        # select_best_vision_model()) and warming up the model (a real GPU
        # load) both have real cost/failure modes, so this is only called
        # once each branch below has confirmed there's actual work to do --
        # a no-op run (nothing new to process) must stay a true no-op, same
        # as it already is for gpt/gemini, instead of needlessly contacting
        # Ollama or loading a multi-GB model just to then do nothing with it.
        nonlocal _vision_model, _ollama_resolved
        if _ollama_resolved:
            return
        if config.ollama_vision_model:
            _vision_model = config.ollama_vision_model
        else:
            # Raises RuntimeError (caught by cli.py/cli_main.py's main()) if
            # Ollama is unreachable, has no vision-capable models pulled, or
            # none fit in currently-free VRAM.
            from visual_parser.ollama_local import select_best_vision_model
            _vision_model = select_best_vision_model()
            print(f"[OLLAMA] Auto-selected vision model: {_vision_model}")

        # Force the load now (one request) rather than letting the first of
        # several concurrent Step 2 workers absorb Ollama's cold-load delay,
        # then report whether it actually landed on GPU or CPU -- the
        # OpenAI-compatible endpoint used for the real calls has no way to
        # surface this; Ollama's own /api/ps does.
        from visual_parser.ollama_local import (
            describe_gpu_status,
            get_loaded_model_gpu_status,
            warm_up_model,
        )
        print(f"[OLLAMA] Loading {_vision_model} …")
        warm_up_model(_vision_model)
        print(f"[OLLAMA] {_vision_model}: {describe_gpu_status(get_loaded_model_gpu_status(_vision_model))}")
        _ollama_resolved = True

    # Nougat and a local Ollama vision model both compete for the same GPU.
    # Loading Ollama's model up front would force Nougat to compete for
    # whatever VRAM is left over, defeating the point of releasing Nougat's
    # memory below before the vision steps run. Defer the load until after
    # Nougat has run and released its memory instead -- but only for this one
    # combination: cloud providers never touch local GPU, skip-text mode
    # never runs Nougat at all, and lightweight text extraction never touches
    # the GPU either, so none of those need deferring.
    _defer_ollama_warm_up = (
        config.vision_provider == "ollama"
        and config.text_mode == "nougat"
        and not config.skip_text
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

        if config.vision_provider == "ollama":
            _ensure_ollama_vision_model()  # never deferred here -- skip-text never runs Nougat

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
            max_workers      = config.max_workers,
            context_pages    = config.vision_context_pages,
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

        if not new_pdfs and not config.rebuild:
            recovered = _recover_stale_registry_entries(config.input_dir, output_dir, registry_path)
            if recovered:
                new_pdfs = find_new_pdfs(config.input_dir, rebuild=False)
                summary["new_pdfs_found"] = len(new_pdfs)

        if not new_pdfs:
            print("No new PDFs found. Nothing to do.")
            return summary

        print(f"Found {len(new_pdfs)} new PDF(s). Starting pipeline …")

        if config.vision_provider == "ollama" and not _defer_ollama_warm_up:
            _ensure_ollama_vision_model()

        def _run_metadata_extraction() -> Dict[str, dict]:
            meta_map: Dict[str, dict] = {}
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
                    meta_map[pdf_path] = meta
                except Exception as exc:
                    logger.warning("Metadata extraction failed for %s: %s", pdf_path, exc)
                    meta_map[pdf_path] = {"_error": str(exc)}
            return meta_map

        # Step 0.5 — Metadata extraction (deferred until after Step 1 for the
        # ollama+nougat combination -- see _defer_ollama_warm_up above)
        if not _defer_ollama_warm_up:
            pdf_meta_map = _run_metadata_extraction()

        # Step 1 — Text extraction and chunking
        processor = model = device = None  # only bound by the "nougat" branch below
        if config.text_mode == "nougat":
            print("[Step 1] Running Nougat text extraction …")
            from visual_parser.nougat_engine import NougatInitializer
            from visual_parser.text_extractor import lightweight_extract_pdfs, nougat_extract_pdfs

            try:
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
                    rebuild            = config.rebuild,
                )
                print(nougat_summary)
            except Exception as exc:
                logger.error("Nougat initialization/extraction failed: %s", exc)
                print(f"[Step 1] Nougat failed ({exc}). Falling back to lightweight extraction.")
                lw_summary, processed_basenames, failed_basenames, chunk_count = lightweight_extract_pdfs(
                    only_process_these = new_pdfs,
                    output_dir         = output_dir,
                    chunk_size         = config.chunk_size,
                    chunk_overlap      = config.chunk_overlap,
                    max_workers        = config.max_workers,
                    rebuild            = config.rebuild,
                )
                print(lw_summary)
            else:
                if failed_basenames:
                    failed_set = set(failed_basenames)
                    remaining = [p for p in new_pdfs if os.path.basename(p) in failed_set]
                    logger.warning(
                        "Nougat produced no text for %d PDF(s). Falling back to lightweight extraction.",
                        len(remaining),
                    )
                    lw_summary, lw_processed, lw_failed, lw_chunk_count = lightweight_extract_pdfs(
                        only_process_these = remaining,
                        output_dir         = output_dir,
                        chunk_size         = config.chunk_size,
                        chunk_overlap      = config.chunk_overlap,
                        max_workers        = config.max_workers,
                        rebuild            = config.rebuild,
                    )
                    print(lw_summary)
                    processed_basenames.extend(lw_processed)
                    failed_basenames = [name for name in failed_basenames if name not in set(lw_processed)]
                    chunk_count += lw_chunk_count

        else:  # "lightweight"
            print("[Step 1] Running lightweight (PyMuPDF) text extraction …")
            from visual_parser.text_extractor import lightweight_extract_pdfs

            lw_summary, processed_basenames, failed_basenames, chunk_count = lightweight_extract_pdfs(
                only_process_these = new_pdfs,
                output_dir         = output_dir,
                chunk_size         = config.chunk_size,
                chunk_overlap      = config.chunk_overlap,
                max_workers        = config.max_workers,
                rebuild            = config.rebuild,
            )
            print(lw_summary)

        summary["processed_basenames"] = processed_basenames
        summary["failed_basenames"]    = failed_basenames
        summary["text_chunks_written"] = chunk_count

        # Nougat is done with the GPU by now (Step 1 has fully completed,
        # success or fallback) but its model otherwise stays resident in
        # VRAM for the rest of this function's scope -- release it before
        # Step 2 so the vision step (and any local Ollama model it loads)
        # has that memory available instead.
        if model is not None:
            del processor, model
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        if _defer_ollama_warm_up:
            # Now that Nougat has released the GPU, resolve/load the Ollama
            # vision model and run the metadata extraction deferred above.
            _ensure_ollama_vision_model()
            pdf_meta_map = _run_metadata_extraction()

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
                max_workers      = config.max_workers,
                context_pages    = config.vision_context_pages,
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
