"""
jsonl_writer.py — Atomic JSONL append helper and stable document-ID generator.

Consolidated from the two duplicate copies that existed in
utils/nougat_helpers.py and PDFAnalyser.py.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Dict, List

logger = logging.getLogger(__name__)


def make_document_id(source: str) -> str:
    """
    Return a 16-character hex SHA-1 digest of the PDF basename.

    The ID is stable across runs as long as the filename doesn't change,
    which lets downstream systems deduplicate without re-reading JSONL files.
    """
    try:
        return hashlib.sha1(source.encode("utf-8")).hexdigest()[:16]
    except Exception as exc:
        logger.warning("Could not hash source %r: %s — using raw name as fallback.", source, exc)
        return source


def append_to_jsonl(jsonl_file: str, new_data: List[Dict]) -> None:
    """
    Safely append *new_data* to a JSON Lines file.

    - Creates the file (and any missing parent directories) if needed.
    - Skips individual rows that cannot be serialised without aborting the
      entire write.
    - Never corrupts existing content: each row is appended as a complete
      ``\\n``-terminated JSON line.

    Args:
        jsonl_file: Absolute or relative path to the target ``.jsonl`` file.
        new_data:   List of dicts to write (one per line).
    """
    if not isinstance(new_data, list):
        logger.warning(
            "append_to_jsonl: new_data must be a list, got %s — skipping.",
            type(new_data).__name__,
        )
        return

    try:
        parent = os.path.dirname(jsonl_file)
        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(jsonl_file, "a", encoding="utf-8") as fh:
            for row in new_data:
                if not isinstance(row, dict):
                    logger.warning("Skipping non-dict JSONL entry: %s", type(row).__name__)
                    continue
                try:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                except (TypeError, ValueError) as exc:
                    logger.warning("Failed to serialise row — skipping. Error: %s", exc)

    except OSError as exc:
        logger.error("File-system error writing %s: %s", jsonl_file, exc)
    except Exception as exc:
        logger.error("Unexpected error writing %s: %s", jsonl_file, exc)


def read_jsonl(jsonl_path: str) -> List[Dict]:
    """
    Read all valid JSON lines from *jsonl_path*.

    Corrupted lines are skipped with a warning; the rest are returned intact.
    """
    rows: List[Dict] = []
    if not os.path.exists(jsonl_path):
        logger.warning("JSONL file not found: %s", jsonl_path)
        return rows

    try:
        with open(jsonl_path, "r", encoding="utf-8") as fh:
            for line_num, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    logger.warning(
                        "Skipping corrupted JSONL line %d in %s: %s",
                        line_num, jsonl_path, exc,
                    )
    except Exception as exc:
        logger.error("Error reading %s: %s", jsonl_path, exc)

    return rows
