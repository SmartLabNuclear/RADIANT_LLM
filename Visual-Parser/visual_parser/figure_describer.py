"""
figure_describer.py — Rasterise every page of each PDF at high DPI and send
                      each page image to a Vision LLM for figure extraction.

Extracted and cb-decoupled from the inner ``describe_figures_for_new_pdfs``
function in PDFAnalyser.py.

Output
------
One record per figure (or per page that contains at least one figure) is
appended to ``02_visuals_kb.jsonl`` in *output_dir*:

    {
        "source":        "myreport.pdf",
        "page":          3,
        "document_id":   "a1b2c3d4e5f6g7h8",
        "figure_index":  0,
        "figure_id":     "a1b2c3d4e5f6g7h8:p3:f0",
        "description":   "**Subject:** ...",
        "vision_provider": "gpt",
        "vision_model":    "gpt-5.4"
    }
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from visual_parser import pdf_engine
from visual_parser.jsonl_writer import append_to_jsonl, make_document_id
from visual_parser.prompts import FIGURE_PROMPT, build_figure_prompt_with_context
from visual_parser.vision_llm import call_vision_llm

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# JSON response parser
# ---------------------------------------------------------------------------

def _parse_llm_response(
    raw: str,
    pdf_name: str,
    page_number: Optional[int] = None,
) -> Optional[List[Dict]]:
    """
    Parse the Vision LLM's JSON list response.

    Strips markdown fences, tries ``json.loads``, then falls back to a regex
    search for a JSON array if the model wraps it in prose.
    """
    body = raw.strip()
    for fence in ("```json", "```"):
        body = body.replace(fence, "")

    try:
        return json.loads(body)
    except json.JSONDecodeError:
        match = re.search(r"(\[\s*\{.*?\}\s*\])", body, re.S)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        label = f"{pdf_name} p{page_number}" if page_number else pdf_name
        logger.warning("Could not parse JSON for %s: %r", label, body[:200])
        return None


# ---------------------------------------------------------------------------
# Main function
# ---------------------------------------------------------------------------

def describe_figures_for_new_pdfs(
    new_pdf_paths: List[str],
    output_dir: str,
    vision_provider: str,
    vision_api_key: str,
    vision_model: str,
    vision_detail: str = "low",
    raster_dpi: int = 200,
    figure_prompt: str = FIGURE_PROMPT,
    reasoning_effort: Optional[str] = "medium",
    max_workers: int = 4,
    context_pages: int = 0,
) -> List[str]:
    """
    For each PDF in *new_pdf_paths*, rasterise every page at *raster_dpi* DPI,
    call the Vision LLM for each page (concurrently, up to *max_workers* at
    once), parse the figure descriptions, and append the results to
    ``02_visuals_kb.jsonl`` in *output_dir*.

    Args:
        new_pdf_paths:    Full paths of PDFs to describe.
        output_dir:       Directory where ``02_visuals_kb.jsonl`` is written.
        vision_provider:  ``'gpt'``, ``'gemini'``, or ``'ollama'``.
        vision_api_key:   API key for the chosen provider (unused for ollama).
        vision_model:     Vision model name string.
        vision_detail:    Image detail level (GPT only).
        raster_dpi:       DPI used when rasterising pages.  200 DPI gives a
                          good balance between quality and API payload size.
        figure_prompt:    The instruction prompt sent with each page image.
                          Override this to customise for a specific domain.
        max_workers:      Thread-pool size for concurrent vision-LLM calls
                          (these are network-bound cloud/local-API calls, not
                          local compute, so thread concurrency is the right
                          primitive -- same as text_extractor.py's PDF-level
                          parallelism).
        context_pages:    Number of adjacent pages (before and after) to send
                          alongside each target page, to help the model
                          interpret a figure/caption that spans a page break.
                          0 (default) reproduces the exact single-page
                          behavior this function had before this parameter
                          existed.

    Always resumes from 02_visuals_kb.jsonl's existing content (page-level,
    via the done_pages set below) -- callers that want a page redescribed
    must first remove its existing row(s) (see kb_redo.redo_entries()) and
    its basename from the processed-PDFs registry, then pass it in here as
    if new; this function has no bypass of its own, so there is no path to
    producing a duplicate row.

    Each written row also carries ``vision_provider``/``vision_model``, so a
    document resumed later under a different model is detectable. Detection
    is active, not just recorded after the fact: if a PDF already has rows
    from a *different* vision_model than this call's, its remaining pages
    are skipped entirely (not mixed in under the new model) and its basename
    is returned, so a resumed document never silently ends up with figures
    described by two different models. Pre-upgrade rows with no recorded
    vision_model are treated as unknown, not a mismatch, and do not block.
    Callers that want the document redescribed consistently under the new
    model must first clear it (see kb_redo.redo_entries(), e.g. via --redo).

    Returns:
        Basenames skipped in full due to a detected vision_model mismatch
        against their existing rows (empty list when none were skipped).
    """
    # -----------------------------------------------------------------------
    # Step 1 – Rasterise every page of every new PDF
    # -----------------------------------------------------------------------
    page_images: List[Dict[str, Any]] = []

    for pdf_full_path in new_pdf_paths:
        pdf_name = os.path.basename(pdf_full_path)
        try:
            with pdf_engine.open_pdf(pdf_full_path) as pdf:
                for page_index in range(pdf.page_count):
                    page_images.append({
                        "pdf":   pdf_name,
                        "page":  page_index + 1,
                        "bytes": pdf.render_png(page_index, dpi=raster_dpi),
                    })
        except Exception as exc:
            logger.error("Error rasterising %s: %s", pdf_name, exc)

    if not page_images:
        logger.info("No pages to describe (all PDFs failed to rasterise).")
        return []

    # -----------------------------------------------------------------------
    # Step 2 – Group page images by PDF name. Order within each group is
    #          page order (enumerate(doc) appended them in order) -- this
    #          ordering is what lets context-page windows below be sliced
    #          directly from each group without re-sorting.
    # -----------------------------------------------------------------------
    pages_by_pdf: Dict[str, List[Dict]] = defaultdict(list)
    for record in page_images:
        pages_by_pdf[record["pdf"]].append(record)

    # -----------------------------------------------------------------------
    # Step 2.5 – Build set of (source, page) pairs already on disk so a
    #            mid-run crash can be resumed at page granularity.
    # -----------------------------------------------------------------------
    figures_path = os.path.join(output_dir, "02_visuals_kb.jsonl")
    done_pages: set = set()
    prior_models_by_pdf: Dict[str, set] = defaultdict(set)
    if os.path.exists(figures_path):
        with open(figures_path, encoding="utf-8") as _fh:
            for _line in _fh:
                _line = _line.strip()
                if not _line:
                    continue
                try:
                    _rec = json.loads(_line)
                    _src = _rec.get("source", "")
                    _pg  = _rec.get("page")
                    if _src and _pg is not None:
                        done_pages.add((_src, _pg))
                    _prior_model = _rec.get("vision_model")
                    if _src and _prior_model:
                        prior_models_by_pdf[_src].add(_prior_model)
                except Exception:
                    pass
    if done_pages:
        logger.info(
            "Resuming: %d page(s) already in 02_visuals_kb.jsonl — will skip.",
            len(done_pages),
        )

    # -----------------------------------------------------------------------
    # Step 3 – Build one task per not-already-done target page. Each task's
    #          image window is sliced from the same PDF's page list only --
    #          never crosses into a different PDF.
    # -----------------------------------------------------------------------
    tasks: List[Dict[str, Any]] = []
    model_mismatch_skipped: List[str] = []
    for pdf_name, image_records in pages_by_pdf.items():
        prior_models = prior_models_by_pdf.get(pdf_name)
        if prior_models and vision_model not in prior_models:
            msg = (
                f"[FIGURES] Skipping {pdf_name}: already has figures described with "
                f"{', '.join(sorted(prior_models))}, but this run is using {vision_model}. "
                f"Run with --redo {pdf_name} to reprocess it entirely under the new model."
            )
            logger.error(msg)
            print(msg)
            model_mismatch_skipped.append(pdf_name)
            continue

        for idx, record in enumerate(image_records):
            page_number = record["page"]
            if (pdf_name, page_number) in done_pages:
                logger.debug("Skipping %s page %d (already in KB).", pdf_name, page_number)
                continue

            window_start = max(0, idx - context_pages)
            window_end   = min(len(image_records), idx + context_pages + 1)
            window       = image_records[window_start:window_end]
            target_index_in_window = idx - window_start

            tasks.append({
                "pdf_name":     pdf_name,
                "page_number":  page_number,
                "images":       [w["bytes"] for w in window],
                "target_index": target_index_in_window,
                "total_images": len(window),
            })

    if not tasks:
        logger.info("No new pages to describe — all already processed.")
        return model_mismatch_skipped

    # -----------------------------------------------------------------------
    # Step 4 – Call Vision LLM per task, concurrently. Each worker only
    #          computes and returns a result; only the single-threaded
    #          completion loop below calls append_to_jsonl, so the file is
    #          never written to from more than one thread at a time (writing
    #          it directly from workers would not be safe -- append_to_jsonl
    #          opens the file fresh per call and buffers multi-line writes).
    # -----------------------------------------------------------------------
    def _describe_one(task: Dict[str, Any]) -> Dict[str, Any]:
        pdf_name    = task["pdf_name"]
        page_number = task["page_number"]
        prompt = build_figure_prompt_with_context(
            figure_prompt, task["target_index"], task["total_images"]
        )
        try:
            raw_response = call_vision_llm(
                images=task["images"],
                prompt=prompt,
                provider=vision_provider,
                api_key=vision_api_key,
                model=vision_model,
                detail=vision_detail,
                reasoning_effort=reasoning_effort,
            )

            captions = _parse_llm_response(raw_response, pdf_name, page_number)
            if isinstance(captions, dict):
                captions = [captions]
            if not isinstance(captions, list):
                logger.warning(
                    "Vision LLM returned non-list output for %s page %d",
                    pdf_name, page_number,
                )
                return {"pdf_name": pdf_name, "page_number": page_number, "rows": []}

            document_id = make_document_id(pdf_name)
            page_rows: List[Dict] = []
            for fig_idx, caption in enumerate(captions):
                if not isinstance(caption, dict):
                    continue
                description = caption.get("description")
                if not isinstance(description, str):
                    logger.warning(
                        "Figure %d on %s page %d has a non-string 'description' "
                        "(got %s) -- model likely returned a malformed/nested "
                        "response; skipping.",
                        fig_idx, pdf_name, page_number, type(description).__name__,
                    )
                    continue
                page_rows.append({
                    "source":          pdf_name,
                    "page":            page_number,
                    "document_id":     document_id,
                    "figure_index":    fig_idx,
                    "figure_id":       f"{document_id}:p{page_number}:f{fig_idx}",
                    "description":     description,
                    "vision_provider": vision_provider,
                    "vision_model":    vision_model,
                })
            return {"pdf_name": pdf_name, "page_number": page_number, "rows": page_rows}

        except Exception as exc:
            logger.error(
                "Vision LLM failed for %s page %d: %s",
                pdf_name, page_number, exc,
            )
            return {"pdf_name": pdf_name, "page_number": page_number, "rows": []}

    total_written = 0
    written_by_pdf: Dict[str, int] = defaultdict(int)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_describe_one, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                logger.error(
                    "Error collecting result for %s page %d: %s",
                    task["pdf_name"], task["page_number"], exc,
                )
                continue

            page_rows = result["rows"]
            if page_rows:
                append_to_jsonl(figures_path, page_rows)
                written_by_pdf[result["pdf_name"]] += len(page_rows)
                total_written += len(page_rows)

    for pdf_name, count in written_by_pdf.items():
        logger.info("[FIGURES] %s: %d figure(s) written.", pdf_name, count)
    for pdf_name in pages_by_pdf:
        if pdf_name not in written_by_pdf and pdf_name not in model_mismatch_skipped:
            logger.info("[FIGURES] %s: no new figures (all pages done or none detected).", pdf_name)

    if total_written:
        print(f"[FIGURES] Wrote {total_written} figure record(s) to 02_visuals_kb.jsonl.")
    else:
        logger.info("No new figures written — all pages already processed or none detected.")

    return model_mismatch_skipped
