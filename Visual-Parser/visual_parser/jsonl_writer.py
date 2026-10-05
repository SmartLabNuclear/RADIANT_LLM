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
from typing import Callable, Dict, List

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


def append_to_jsonl(jsonl_file: str, new_data: List[Dict]) -> bool:
    """
    Safely append *new_data* to a JSON Lines file.

    - Creates the file (and any missing parent directories) if needed.
    - Skips individual rows that cannot be serialised without aborting the
      entire write.
    - Never corrupts existing content: each row is appended as a complete
      ``\\n``-terminated JSON line.

    Returns True if the file was opened and written without a file-system-
    level error (even if some individual rows were skipped for being
    unserialisable), False if the write failed entirely (e.g. disk full,
    permissions). No existing caller checked this return value before it was
    added (confirmed: every call site is a bare statement), so adding a
    meaningful value here is backward compatible -- but callers whose own
    resume/registry state depends on the write actually landing (e.g.
    image_describer.py marking an image "processed") should check it instead
    of assuming success, since a caught exception here previously had no way
    to propagate past this function at all.

    Args:
        jsonl_file: Absolute or relative path to the target ``.jsonl`` file.
        new_data:   List of dicts to write (one per line).
    """
    if not isinstance(new_data, list):
        logger.warning(
            "append_to_jsonl: new_data must be a list, got %s — skipping.",
            type(new_data).__name__,
        )
        return False

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
        return True

    except OSError as exc:
        logger.error("File-system error writing %s: %s", jsonl_file, exc)
        return False
    except Exception as exc:
        logger.error("Unexpected error writing %s: %s", jsonl_file, exc)
        return False


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


def atomic_rewrite_jsonl(jsonl_path: str, keep_predicate: Callable[[Dict], bool]) -> Dict[str, int]:
    """
    Rewrite *jsonl_path* in place, keeping only rows where
    ``keep_predicate(row)`` is True.

    Reads line by line, writes kept rows to a temp file, then replaces the
    original atomically via ``os.replace()`` -- deliberately not
    ``shutil.move()``, which on Windows silently degrades to a non-atomic
    copy+delete when the destination already exists (which it always does
    here). Malformed lines are skipped (counted, not kept, not re-written).

    Returns {"removed": int, "kept": int, "malformed": int}. Does nothing
    (all-zero result) if *jsonl_path* doesn't exist.
    """
    if not os.path.exists(jsonl_path):
        return {"removed": 0, "kept": 0, "malformed": 0}

    removed = kept = malformed = 0
    tmp_path = jsonl_path + ".tmp"

    try:
        with open(jsonl_path, "r", encoding="utf-8") as infile, \
             open(tmp_path, "w", encoding="utf-8") as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                if keep_predicate(row):
                    outfile.write(json.dumps(row, ensure_ascii=False) + "\n")
                    kept += 1
                else:
                    removed += 1
        os.replace(tmp_path, jsonl_path)
    except Exception as exc:
        logger.error("Error rewriting %s: %s", jsonl_path, exc)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return {"removed": 0, "kept": 0, "malformed": 0}

    return {"removed": removed, "kept": kept, "malformed": malformed}
