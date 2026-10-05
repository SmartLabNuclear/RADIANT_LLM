"""
pdf_tracker.py — Utilities for detecting new PDFs and persisting the
                 set of already-processed filenames across pipeline runs.

Extracted and cleaned from PDFAnalyser.py.
"""

from __future__ import annotations

import logging
import os
from typing import List

logger = logging.getLogger(__name__)

PROCESSED_REGISTRY = "04_processed_pdfs.txt"


# ---------------------------------------------------------------------------
# Registry I/O
# ---------------------------------------------------------------------------

def sanitize_string(s: str) -> str:
    """Re-encode *s* as UTF-8, replacing any unrepresentable characters."""
    return s.encode("utf-8", errors="replace").decode("utf-8")


def load_processed_pdfs(registry_path: str) -> List[str]:
    """
    Return the list of PDF basenames that have already been processed.

    Falls back to latin-1 decoding when UTF-8 fails (handles legacy files).
    """
    if not os.path.exists(registry_path):
        return []
    try:
        with open(registry_path, "r", encoding="utf-8") as fh:
            return [line for line in fh.read().splitlines() if line.strip()]
    except UnicodeDecodeError:
        logger.warning("UTF-8 decoding failed for %s — retrying with latin-1.", registry_path)
        with open(registry_path, "r", encoding="latin-1") as fh:
            return [line for line in fh.read().splitlines() if line.strip()]


def save_processed_pdfs(registry_path: str, processed_pdfs: List[str]) -> None:
    """Persist the full (deduplicated) list of processed PDF basenames."""
    with open(registry_path, "w", encoding="utf-8") as fh:
        for name in processed_pdfs:
            fh.write(sanitize_string(name) + "\n")


def mark_as_processed(
    registry_path: str,
    newly_processed: List[str],
) -> None:
    """
    Merge *newly_processed* basenames into the existing registry.

    Safe to call even if the registry doesn't exist yet.
    """
    existing = set(load_processed_pdfs(registry_path))
    existing.update(newly_processed)
    save_processed_pdfs(registry_path, sorted(existing))


def unmark_as_processed(registry_path: str, names_to_remove: List[str]) -> int:
    """
    Remove *names_to_remove* basenames from the registry (exact match, same
    case-sensitive convention as load_processed_pdfs/mark_as_processed --
    these are what actually govern registry contents, so this matches them
    rather than the separate .lower()-everywhere convention used elsewhere
    for other, unrelated comparisons).

    Inverse of mark_as_processed. Safe to call even if the registry doesn't
    exist (returns 0). Only rewrites the file when something actually
    matched, unlike mark_as_processed (which always re-saves).

    Returns the number of entries actually removed.
    """
    existing = load_processed_pdfs(registry_path)
    if not existing:
        return 0
    remove_set = set(names_to_remove)
    kept = [name for name in existing if name not in remove_set]
    removed = len(existing) - len(kept)
    if removed:
        save_processed_pdfs(registry_path, sorted(set(kept)))
    return removed


# ---------------------------------------------------------------------------
# PDF discovery
# ---------------------------------------------------------------------------

def find_new_pdfs(
    input_dir: str,
    registry_filename: str = PROCESSED_REGISTRY,
    rebuild: bool = False,
) -> List[str]:
    """
    Walk *input_dir* recursively and return full paths of PDFs that have NOT
    yet been processed.

    Args:
        input_dir:         Root directory to search for ``.pdf`` files.
        registry_filename: Name of the tracking file inside *input_dir*.
        rebuild:           When True, return *all* PDFs regardless of the
                           registry (forces a full re-parse).

    Returns:
        Sorted list of absolute PDF paths.
    """
    registry_path = os.path.join(input_dir, registry_filename)
    processed = set() if rebuild else set(load_processed_pdfs(registry_path))

    new_pdfs = [
        os.path.join(root, filename)
        for root, _, files in os.walk(input_dir)
        for filename in files
        if filename.lower().endswith(".pdf")
        and os.path.basename(filename) not in processed
    ]

    new_pdfs.sort()
    if new_pdfs:
        logger.info("Found %d new PDF(s) to process.", len(new_pdfs))
    else:
        logger.info("No new PDFs detected in %s.", input_dir)

    return new_pdfs
