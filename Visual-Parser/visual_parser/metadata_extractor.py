"""
metadata_extractor.py — Extract document-level metadata (title, authors, DOI …)
                         from the front pages of a PDF using a vision LLM.

Extracted and cb-decoupled from utils/general_utilities.py.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

import pymupdf as fitz  # PyMuPDF -- "fitz" is the deprecated legacy import name

from visual_parser.prompts import METADATA_PROMPT_TEMPLATE
from visual_parser.vision_llm import call_vision_llm

logger = logging.getLogger(__name__)

# METADATA_PROMPT_TEMPLATE's documented schema: plain-string fields vs.
# array-of-string fields. A weak/non-compliant vision model can return a
# wrong-shaped value (e.g. "authors" as a single string instead of a list) --
# validated against this before trusting it, same fix already applied to
# figure_describer.py/image_describer.py's "description" field.
_EXPECTED_STRING_FIELDS = ("title", "publication_date", "report_number", "doi")
_EXPECTED_LIST_FIELDS = ("authors", "keywords")


def _parse_metadata_response(raw: str, pdf_path: str) -> Dict[str, Any]:
    """
    Parse the Vision LLM's single-JSON-object metadata response.

    Mirrors image_describer.py's _parse_single_image_response: a
    json.JSONDecoder().raw_decode() walk (tries decoding starting at each '{'
    in turn, taking the first span that parses as valid JSON) rather than a
    naive find("{")/rfind("}") substring -- the naive approach breaks if the
    model's surrounding prose has a stray brace character before the real
    JSON object. Also defensively unwraps the case where a model wraps the
    single expected object in a one-element list anyway.
    """
    body = raw.strip()
    for fence in ("```json", "```"):
        body = body.replace(fence, "")

    parsed: Any = None
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        start = body.find("{")
        while start != -1:
            try:
                parsed, _ = decoder.raw_decode(body, start)
                break
            except json.JSONDecodeError:
                start = body.find("{", start + 1)

    if isinstance(parsed, list) and len(parsed) == 1:
        parsed = parsed[0]

    if isinstance(parsed, dict):
        return parsed

    raise RuntimeError(f"No JSON object found in vision LLM response for {pdf_path!r}:\n{raw}")


def _validate_metadata_fields(parsed: Dict[str, Any], pdf_path: str) -> Dict[str, Any]:
    """
    Drop any field whose type doesn't match METADATA_PROMPT_TEMPLATE's
    documented schema, logging a warning for each one dropped, rather than
    silently writing a wrong-shaped value into 03_metadata_kb.jsonl -- a
    malformed "authors" (string instead of list) or "keywords" (dict instead
    of list) wouldn't crash anything in this package (dict.update() and JSONL
    serialization don't care about field shape), but would corrupt the
    knowledge base for whatever downstream system actually consumes it.
    Unknown/extra fields the model invented beyond the documented schema are
    passed through unchanged -- there's no basis to judge their shape.
    """
    validated: Dict[str, Any] = {}
    for key, value in parsed.items():
        if key in _EXPECTED_STRING_FIELDS:
            if isinstance(value, str):
                validated[key] = value
            else:
                logger.warning(
                    "Metadata field '%s' for %s is not a string (got %s) -- "
                    "dropping, model likely returned a malformed response.",
                    key, pdf_path, type(value).__name__,
                )
        elif key in _EXPECTED_LIST_FIELDS:
            if isinstance(value, list) and all(isinstance(v, str) for v in value):
                validated[key] = value
            else:
                logger.warning(
                    "Metadata field '%s' for %s is not a list of strings (got %s) -- "
                    "dropping, model likely returned a malformed response.",
                    key, pdf_path, type(value).__name__,
                )
        else:
            validated[key] = value
    return validated


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

    # 4) Extract and parse the JSON object, then validate field types against
    #    METADATA_PROMPT_TEMPLATE's documented schema.
    parsed = _parse_metadata_response(raw, pdf_path)
    return _validate_metadata_fields(parsed, pdf_path)
