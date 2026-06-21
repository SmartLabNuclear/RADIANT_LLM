"""
metadata_extractor.py — Extract document-level metadata (title, authors, DOI …)
                         from the front pages of a PDF using a vision LLM.

Extracted and cb-decoupled from utils/general_utilities.py.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

import fitz  # PyMuPDF

from visual_parser.prompts import METADATA_PROMPT_TEMPLATE
from visual_parser.vision_llm import call_vision_llm

logger = logging.getLogger(__name__)


def extract_pdf_metadata(
    pdf_path: str,
    vision_provider: str,
    vision_api_key: str,
    vision_model: str,
    num_pages: int = 2,
    vision_detail: str = "auto",
    reasoning_effort: Optional[str] = "medium",
) -> Dict[str, Any]:
    """
    Rasterize the first *num_pages* of *pdf_path*, send them to the Vision LLM,
    and parse the JSON metadata response.

    Args:
        pdf_path:         Absolute path to the PDF file.
        vision_provider:  ``'gpt'`` or ``'gemini'``.
        vision_api_key:   API key for the chosen provider.
        vision_model:     Model name string.
        num_pages:        How many front pages to send (default: 2).
        vision_detail:    Image detail level for GPT ('low', 'high', 'auto').

    Returns:
        Dict with any of: title, authors, publication_date, report_number,
        doi, keywords — plus a ``_source`` entry with the PDF basename.

    Raises:
        RuntimeError on unrecoverable errors (PDF open failure, no valid JSON).
    """
    # 1) Rasterize front pages
    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        raise RuntimeError(f"Failed to open PDF {pdf_path!r}: {exc}") from exc

    images: List[bytes] = []
    for i in range(min(num_pages, doc.page_count)):
        try:
            pix = doc.load_page(i).get_pixmap(dpi=200)
            images.append(pix.tobytes("png"))
        except Exception as exc:
            logger.warning("Skipping page %d of %s: %s", i, pdf_path, exc)
    doc.close()

    if not images:
        raise RuntimeError(f"No pages rendered from {pdf_path!r}")

    # 2) Build prompt
    prompt = METADATA_PROMPT_TEMPLATE.format(num_pages=num_pages)

    # 3) Call Vision LLM
    raw = call_vision_llm(
        images=images,
        prompt=prompt,
        provider=vision_provider,
        api_key=vision_api_key,
        model=vision_model,
        detail=vision_detail,
        reasoning_effort=reasoning_effort,
    )

    # 4) Extract and parse JSON substring
    start = raw.find("{")
    end   = raw.rfind("}")
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError(f"No JSON found in vision LLM response:\n{raw}")

    candidate = raw[start: end + 1].strip().strip("```").strip()
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Failed to parse metadata JSON:\n{candidate}\nError: {exc}"
        ) from exc
