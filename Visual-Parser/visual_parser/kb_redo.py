"""
kb_redo.py — Surgically clear a set of PDF/image basenames from every KB
             JSONL file and both processed-registries, so normal discovery
             naturally reprocesses them as new -- with no duplicate rows,
             unlike blindly reprocessing over an already-populated KB.

Backs this session's --redo NAME flag and --rebuild's internals (--rebuild
gathers every basename currently in --input-dir and runs them all through
this same function before reprocessing, instead of forcing every write path
to bypass its own resume check and silently duplicate rows).

Reimplements (does not import -- visual-parser is a standalone,
dependency-free package and cannot depend on the sibling RADIANT-LLM repo)
the proven basename-match + backup-once + atomic-rewrite pattern from
RADIANT-LLM's knowledge_base_sanitizer() (radiant_lmm/RADIANT_LLM_ChatBot_
Local/utils/pdf_helpers.py:1464-1607), extended to the 4th JSONL file
(image_descriptions_kb.jsonl) and both registries (04_processed_pdfs.txt,
parsed_images.txt), which that function never touches at all.
"""

from __future__ import annotations

import logging
import os
import shutil
from typing import Any, Dict, Iterable, List

from visual_parser.image_describer import IMAGE_DESCRIPTIONS_FILE
from visual_parser.image_tracker import PROCESSED_IMAGES_REGISTRY
from visual_parser.jsonl_writer import atomic_rewrite_jsonl
from visual_parser.pdf_tracker import PROCESSED_REGISTRY, load_processed_pdfs, unmark_as_processed

logger = logging.getLogger(__name__)

# Hardcoded, not glob("*.jsonl") like the RADIANT precedent -- output_dir
# often equals input_dir (the documented default), so globbing risks
# touching unrelated JSONL files a user happens to keep there. The image
# filename is imported (not hardcoded like the other three) because it was
# renamed once already (image_descriptions.jsonl -> image_descriptions_kb.jsonl,
# 2.2.3) with this exact file as a hardcoded duplicate that needed a manual
# fix -- importing the constant means it can't drift out of sync again.
KB_JSONL_FILENAMES = (
    "01_chunks_kb.jsonl",
    "02_visuals_kb.jsonl",
    "03_metadata_kb.jsonl",
    IMAGE_DESCRIPTIONS_FILE,
)
REGISTRY_FILENAMES = (PROCESSED_REGISTRY, PROCESSED_IMAGES_REGISTRY)
BACKUP_SUFFIX = "_backup_before_redo"


def _backup_once(path: str) -> bool:
    """
    Create a one-time backup of *path* if it doesn't already exist.

    Persists forever across repeated calls -- the backup always reflects
    the oldest pre-redo state in the KB's history, not "before this
    particular run" (same convention as the RADIANT precedent).

    Returns True if a backup was created just now.
    """
    stem, ext = os.path.splitext(path)
    backup_path = f"{stem}{BACKUP_SUFFIX}{ext}"
    if os.path.exists(backup_path):
        return False
    shutil.copy2(path, backup_path)
    return True


def redo_entries(output_dir: str, names: Iterable[str]) -> Dict[str, Any]:
    """
    Strip every row/registry-entry belonging to *names* (PDF or image
    basenames, matched case-sensitively, path-stripped) from all 4 KB JSONL
    files and both registries in *output_dir*.

    Treats all 4 JSONL files uniformly -- filters by exact basename match on
    'source' in every file regardless of whether a name is conceptually "a
    PDF" or "an image": every write site in the package always writes
    'source' as a bare os.path.basename(...) result, never a path, and a
    basename can only belong to one real file at a time, so there's no
    cross-type collision risk. Type-agnostic filtering is simpler and
    strictly correct either way.

    Does NOT reprocess anything -- callers must invoke this BEFORE
    discovery (find_new_pdfs()/find_new_images()) so the now-registry-absent
    names are naturally picked back up as new, in the same run.
    """
    name_set = {os.path.basename(n) for n in names if str(n).strip()}

    result: Dict[str, Any] = {
        "output_dir": output_dir,
        "names_requested": sorted(name_set),
        "jsonl_files": [],
        "registries": [],
    }

    names_found: set = set()
    total_rows_removed = 0

    for filename in KB_JSONL_FILENAMES:
        path = os.path.join(output_dir, filename)
        if not os.path.exists(path):
            result["jsonl_files"].append({"file": path, "exists": False})
            continue

        backup_created = _backup_once(path)

        matched_here: set = set()

        def _keep(row: Dict) -> bool:
            source = row.get("source")
            if source in name_set:
                matched_here.add(source)
                return False
            return True

        stats = atomic_rewrite_jsonl(path, _keep)
        names_found |= matched_here
        total_rows_removed += stats["removed"]
        result["jsonl_files"].append({
            "file": path,
            "exists": True,
            "backup_created": backup_created,
            **stats,
        })

    total_registry_removed = 0
    for filename in REGISTRY_FILENAMES:
        path = os.path.join(output_dir, filename)
        if not os.path.exists(path):
            result["registries"].append({"file": path, "exists": False, "removed": 0})
            continue

        backup_created = _backup_once(path)
        existing = set(load_processed_pdfs(path))
        names_found |= (name_set & existing)

        removed = unmark_as_processed(path, sorted(name_set))
        total_registry_removed += removed
        result["registries"].append({
            "file": path,
            "exists": True,
            "backup_created": backup_created,
            "removed": removed,
        })

    result["cleared"] = sorted(names_found)
    result["not_found"] = sorted(name_set - names_found)
    result["totals"] = {
        "rows_removed": total_rows_removed,
        "registry_entries_removed": total_registry_removed,
    }
    return result
