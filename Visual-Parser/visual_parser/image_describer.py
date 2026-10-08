"""
image_describer.py — Send each standalone image to a Vision LLM for a
                      holistic description, one call per image (no page
                      rasterisation, no context window).

Extracted-pattern sibling of figure_describer.py: same ThreadPoolExecutor +
as_completed concurrency shape (worker only computes/returns; only the single-
threaded completion loop calls append_to_jsonl), but for arbitrary user-
supplied image files instead of PyMuPDF-rasterized PDF pages.

Output
------
One record per image is appended to ``image_descriptions_kb.jsonl`` in
*output_dir*:

    {
        "source":      "diagram1.png",
        "image_id":    "a1b2c3d4e5f6g7h8",
        "title":       "Vertical Parabolic Gate Schematic",
        "description": "**Subject:** ..."
    }
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from typing import Any, Dict, List, Optional

from PIL import Image

from visual_parser.jsonl_writer import append_to_jsonl, make_document_id
from visual_parser.prompts import IMAGE_DESCRIPTION_PROMPT
from visual_parser.vision_llm import call_vision_llm

logger = logging.getLogger(__name__)

IMAGE_DESCRIPTIONS_FILE = "image_descriptions_kb.jsonl"

# Decoupled from figure_describer.py's context-window-scaled formula (10 min
# for 1 image there): IMAGE_DESCRIPTION_PROMPT's "Verbatim Text Content"
# requirement can demand much more generated output than FIGURE_PROMPT ever
# needs, since it asks for full verbatim transcription rather than a bounded
# structured description. Measured directly against this model/hardware: a
# dense, text-heavy page took 594s (9.9 min) for a single, uncontended call --
# real concurrent runs (multiple images via --max-workers) push slower still.
# 900s (15 min) calibrated from that real baseline, not guessed.
_OLLAMA_IMAGE_TIMEOUT_SECONDS = 900.0

_SUBJECT_RE = re.compile(r"\*\*Subject:\*\*\s*(.*?)(?:\n|$)")


# ---------------------------------------------------------------------------
# JSON response parser
# ---------------------------------------------------------------------------

def _parse_single_image_response(raw: str, image_name: str) -> Optional[Dict]:
    """
    Parse the Vision LLM's single-JSON-object response for one image.

    A sibling of figure_describer.py's _parse_llm_response: that function's
    prose-recovery regex is list-shaped (looks for "[...]") and cannot
    recover a bare "{...}" object wrapped in prose, which is the expected
    shape here (one image always yields exactly one description, never a
    list). Also defensively unwraps the inverse case -- a model that ignores
    "NOT a list" and returns a single-element list anyway.
    """
    body = raw.strip()
    for fence in ("```json", "```"):
        body = body.replace(fence, "")

    parsed: Any = None
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        # A regex (greedy or lazy) can't reliably find "the" {...} block: the
        # prompt's own OUTPUT FORMAT section embeds a literal, syntactically
        # valid example object, so a model that echoes it alongside its real
        # answer produces two {...} blocks -- greedy spans both into one
        # invalid blob, while lazy stops at the first literal '}' even if
        # that's just a brace character sitting inside a string value (e.g.
        # a description that quotes set notation like "{A, B, C}"). Properly
        # JSON-aware: try decoding starting at each '{' in turn and take the
        # first one that parses as valid JSON, which correctly treats braces
        # inside quoted strings as plain characters, not structure.
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

    logger.warning("Could not parse JSON for image %s: %r", image_name, body[:200])
    return None


def _flatten_to_rgb(pil_image: Image.Image) -> Image.Image:
    """
    Convert *pil_image* to RGB, compositing any transparency onto a white
    background first.

    Image.convert("RGB") alone does NOT do this -- it just drops the alpha
    channel and exposes whatever RGB values are stored underneath, which are
    commonly zeroed by PNG encoders for fully-transparent pixels. A
    transparent-background PNG (a very common export format for standalone
    diagrams/logos/screenshots -- exactly this feature's target content)
    would silently turn mostly/fully black with no exception or log, giving
    the vision LLM a black image instead of a diagram on a light background.
    """
    has_alpha = pil_image.mode in ("RGBA", "LA") or (
        pil_image.mode == "P" and "transparency" in pil_image.info
    )
    if not has_alpha:
        return pil_image.convert("RGB")

    rgba = pil_image.convert("RGBA")
    background = Image.new("RGB", rgba.size, (255, 255, 255))
    background.paste(rgba, mask=rgba.split()[-1])
    return background


def _derive_title(description: str) -> str:
    """
    Derive a concise title from *description*.

    The prompt's heading 1 is always "**Subject:** [Title]" -- extract it
    directly rather than truncating raw characters. Falls back to the first
    sentence boundary, then a hard cut, if the model didn't follow the format.
    """
    match = _SUBJECT_RE.search(description)
    if match:
        subject = match.group(1).strip()
        if subject:
            return subject

    sentence_end = description.find(". ")
    if 0 < sentence_end <= 150:
        return description[:sentence_end + 1].strip()

    return description[:100].strip()


# ---------------------------------------------------------------------------
# Main function
# ---------------------------------------------------------------------------

def describe_images(
    new_image_paths: List[str],
    output_dir: str,
    vision_provider: str,
    vision_api_key: str,
    vision_model: str,
    vision_detail: str = "low",
    image_prompt: str = IMAGE_DESCRIPTION_PROMPT,
    reasoning_effort: Optional[str] = "medium",
    max_workers: int = 4,
) -> List[str]:
    """
    For each image in *new_image_paths*, call the Vision LLM once (no
    context window -- a single standalone image per call), parse the
    description, and append the result to ``image_descriptions_kb.jsonl`` in
    *output_dir*.

    Returns the basenames actually written a row for -- NOT the full input
    list. Unlike PyMuPDF-rasterized PDF pages (always well-formed), arbitrary
    user-supplied image files can be corrupt, truncated, or unreadable, and a
    failed vision call must not be marked as processed by the caller, or the
    image would silently disappear from future find_new_images() output with
    no row ever written.

    Args:
        new_image_paths:  Full paths of images to describe.
        output_dir:       Directory where ``image_descriptions_kb.jsonl`` is written.
        vision_provider:  ``'gpt'``, ``'gemini'``, or ``'ollama'``.
        vision_api_key:   API key for the chosen provider (unused for ollama).
        vision_model:     Vision model name string.
        vision_detail:    Image detail level (GPT/Ollama only).
        image_prompt:     The instruction prompt sent with each image.
        max_workers:      Thread-pool size for concurrent vision-LLM calls.

    Always resumes from image_descriptions_kb.jsonl's existing content (via the
    done_images set below) -- callers that want an image redescribed must
    first remove its existing row and its basename from the processed-
    images registry (see kb_redo.redo_entries()), then pass it in here as if
    new; this function has no bypass of its own, so there is no path to
    producing a duplicate row.
    """
    descriptions_path = os.path.join(output_dir, IMAGE_DESCRIPTIONS_FILE)

    # -------------------------------------------------------------------
    # Build set of images already on disk (resume safety).
    # -------------------------------------------------------------------
    done_images: set = set()
    if os.path.exists(descriptions_path):
        with open(descriptions_path, encoding="utf-8") as _fh:
            for _line in _fh:
                _line = _line.strip()
                if not _line:
                    continue
                try:
                    _rec = json.loads(_line)
                    _src = _rec.get("source", "")
                    if _src:
                        done_images.add(_src)
                except Exception:
                    pass
    if done_images:
        logger.info(
            "Resuming: %d image(s) already in %s — will skip.",
            len(done_images), IMAGE_DESCRIPTIONS_FILE,
        )

    tasks = [
        {"path": path, "name": os.path.basename(path)}
        for path in new_image_paths
        if os.path.basename(path) not in done_images
    ]

    if not tasks:
        logger.info("No new images to describe — all already processed.")
        return []

    # -------------------------------------------------------------------
    # Call Vision LLM per task, concurrently. Each worker only computes
    # and returns a result; only the single-threaded completion loop below
    # calls append_to_jsonl, so the file is never written to from more
    # than one thread at a time (writing it directly from workers would
    # not be safe -- append_to_jsonl opens the file fresh per call).
    # -------------------------------------------------------------------
    def _describe_one(task: Dict[str, Any]) -> Dict[str, Any]:
        image_name = task["name"]
        try:
            with open(task["path"], "rb") as fh:
                raw_bytes = fh.read()
            # Re-encode to PNG in memory, mirroring figure_describer.py's own
            # pix.tobytes("png") step. Not cosmetic: OpenAI's vision API does
            # not accept BMP or TIFF at all, regardless of what the data: URL
            # claims, so a raw passthrough would fail outright for those.
            pil_image = _flatten_to_rgb(Image.open(BytesIO(raw_bytes)))
            buf = BytesIO()
            pil_image.save(buf, format="PNG")
            png_bytes = buf.getvalue()

            raw_response = call_vision_llm(
                images=[png_bytes],
                prompt=image_prompt,
                provider=vision_provider,
                api_key=vision_api_key,
                model=vision_model,
                detail=vision_detail,
                reasoning_effort=reasoning_effort,
                ollama_timeout_seconds=_OLLAMA_IMAGE_TIMEOUT_SECONDS,
            )

            parsed = _parse_single_image_response(raw_response, image_name)
            if parsed is None:
                return {"image_name": image_name, "row": None}

            description = parsed.get("description")
            if not isinstance(description, str):
                logger.warning(
                    "'description' field for image %s is not a string (got %s) -- "
                    "model likely returned a malformed/nested response; skipping.",
                    image_name, type(description).__name__,
                )
                return {"image_name": image_name, "row": None}

            row = {
                "source":      image_name,
                "image_id":    make_document_id(image_name),
                "title":       _derive_title(description),
                "description": description,
            }
            return {"image_name": image_name, "row": row}

        except Exception as exc:
            logger.error("Vision LLM failed for image %s: %s", image_name, exc)
            return {"image_name": image_name, "row": None}

    written_basenames: List[str] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_describe_one, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                logger.error("Error collecting result for image %s: %s", task["name"], exc)
                continue

            row = result["row"]
            if row is not None:
                # Only mark this basename "written" if the row actually
                # landed on disk -- the caller uses this to persist
                # parsed_images.txt, and unlike the PDF/figure side (which
                # resumes by reading 02_visuals_kb.jsonl's own content back,
                # self-healing after a transient write failure), the image
                # registry is a separate file with no such self-correction.
                # A silently-swallowed disk/permission error here previously
                # still counted as "done" -- permanent data loss with no
                # retry path short of --redo/--rebuild.
                if append_to_jsonl(descriptions_path, [row]):
                    written_basenames.append(result["image_name"])
                else:
                    logger.error(
                        "Failed to write description for %s -- not marking processed, will retry next run.",
                        result["image_name"],
                    )

    if written_basenames:
        print(f"[IMAGES] Wrote {len(written_basenames)} image description(s) to {IMAGE_DESCRIPTIONS_FILE}.")
    else:
        logger.info("No new image descriptions written.")

    return written_basenames
