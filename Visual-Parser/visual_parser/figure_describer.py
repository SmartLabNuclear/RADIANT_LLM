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
        "description":   "**Subject:** ..."
    }
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional

import fitz  # PyMuPDF

from visual_parser.jsonl_writer import append_to_jsonl, make_document_id
from visual_parser.prompts import FIGURE_PROMPT
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
) -> None:
    """
    For each PDF in *new_pdf_paths*, rasterise every page at *raster_dpi* DPI,
    call the Vision LLM page-by-page, parse the figure descriptions, and
    append the results to ``02_visuals_kb.jsonl`` in *output_dir*.

    Args:
        new_pdf_paths:    Full paths of PDFs to describe.
        output_dir:       Directory where ``02_visuals_kb.jsonl`` is written.
        vision_provider:  ``'gpt'`` or ``'gemini'``.
        vision_api_key:   API key for the chosen provider.
        vision_model:     Vision model name string.
        vision_detail:    Image detail level (GPT only).
        raster_dpi:       DPI used when rasterising pages.  200 DPI gives a
                          good balance between quality and API payload size.
        figure_prompt:    The instruction prompt sent with each page image.
                          Override this to customise for a specific domain.
    """
    # -----------------------------------------------------------------------
    # Step 1 – Rasterise every page of every new PDF
    # -----------------------------------------------------------------------
    page_images: List[Dict[str, Any]] = []

    for pdf_full_path in new_pdf_paths:
        pdf_name = os.path.basename(pdf_full_path)
        try:
            doc = fitz.open(pdf_full_path)
            for page_index, page in enumerate(doc):
                pix = page.get_pixmap(dpi=raster_dpi)
                page_images.append({
                    "pdf":   pdf_name,
                    "page":  page_index + 1,
                    "bytes": pix.tobytes("png"),
                })
            doc.close()
        except Exception as exc:
            logger.error("Error rasterising %s: %s", pdf_name, exc)

    if not page_images:
        logger.info("No pages to describe (all PDFs failed to rasterise).")
        return

    # -----------------------------------------------------------------------
    # Step 2 – Group page images by PDF name
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
                except Exception:
                    pass
    if done_pages:
        logger.info(
            "Resuming: %d page(s) already in 02_visuals_kb.jsonl — will skip.",
            len(done_pages),
        )

    # -----------------------------------------------------------------------
    # Step 3 – Call Vision LLM per page; flush each page to disk immediately.
    #          Figure records are independent so per-page atomicity is safe.
    # -----------------------------------------------------------------------
    total_written = 0

    for pdf_name, image_records in pages_by_pdf.items():
        pdf_written = 0

        for record in image_records:
            page_number = record["page"]
            image_bytes = record["bytes"]

            if (pdf_name, page_number) in done_pages:
                logger.debug("Skipping %s page %d (already in KB).", pdf_name, page_number)
                continue

            try:
                raw_response = call_vision_llm(
                    images=[image_bytes],
                    prompt=figure_prompt,
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
                    continue

                document_id = make_document_id(pdf_name)
                page_rows: List[Dict] = []
                for fig_idx, caption in enumerate(captions):
                    if not isinstance(caption, dict):
                        continue
                    description = caption.get("description")
                    if description is None:
                        continue
                    page_rows.append({
                        "source":       pdf_name,
                        "page":         page_number,
                        "document_id":  document_id,
                        "figure_index": fig_idx,
                        "figure_id":    f"{document_id}:p{page_number}:f{fig_idx}",
                        "description":  description,
                    })

                if page_rows:
                    append_to_jsonl(figures_path, page_rows)
                    pdf_written   += len(page_rows)
                    total_written += len(page_rows)

            except Exception as exc:
                logger.error(
                    "Vision LLM failed for %s page %d: %s",
                    pdf_name, page_number, exc,
                )

        if pdf_written:
            logger.info("[FIGURES] %s: %d figure(s) written.", pdf_name, pdf_written)
        else:
            logger.info("[FIGURES] %s: no new figures (all pages done or none detected).", pdf_name)

    if total_written:
        print(f"[FIGURES] Wrote {total_written} figure record(s) to 02_visuals_kb.jsonl.")
    else:
        logger.info("No new figures written — all pages already processed or none detected.")
