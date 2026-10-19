#!/usr/bin/env python3
"""CLI check: is radiant_llm_skills/MANIFEST.json current for this tree?

Reuses generate_skill_manifest.generate_manifest() (the exact file-set/hash
rules the manifest itself is built from) rather than reimplementing hashing.

Exits non-zero and lists every drifted/new/removed file if the manifest is
stale. Intended as a pre-commit gate (see .githooks/pre-commit) and as a
manual check after editing anything under radiant_llm_skills/.

Usage:
    python maintenance_scripts/check_skill_manifest_freshness.py
    python maintenance_scripts/check_skill_manifest_freshness.py --root /path/to/radiant_llm_skills
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from generate_skill_manifest import generate_manifest  # noqa: E402


def load_manifest(bundled_root: Path) -> dict[str, str]:
    manifest_path = bundled_root / "MANIFEST.json"
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items()}
    except Exception:
        pass
    return {}


def main() -> int:
    args = sys.argv[1:]
    if "--root" in args:
        root = Path(args[args.index("--root") + 1]).resolve()
    else:
        # radiant_llm_skills/ sits at the repo root, a sibling of maintenance_scripts/.
        root = (_SCRIPT_DIR.parent / "radiant_llm_skills").resolve()

    if not root.is_dir():
        print(f"[ERROR] radiant_llm_skills not found at: {root}", file=sys.stderr)
        return 1

    current = generate_manifest(root)
    recorded = load_manifest(root)

    changed = sorted(p for p in current if p in recorded and current[p] != recorded[p])
    new = sorted(p for p in current if p not in recorded)
    removed = sorted(p for p in recorded if p not in current)

    if not changed and not new and not removed:
        print(f"MANIFEST.json is current ({len(current)} file(s)) for: {root}")
        return 0

    print(f"[STALE] MANIFEST.json does not match the current content of: {root}")
    if changed:
        print(f"\n  Changed since last manifest regeneration ({len(changed)}):")
        for p in changed:
            print(f"    {p}")
    if new:
        print(f"\n  New, not yet in manifest ({len(new)}):")
        for p in new:
            print(f"    {p}")
    if removed:
        print(f"\n  Recorded in manifest but no longer present ({len(removed)}):")
        for p in removed:
            print(f"    {p}")
    print(
        "\nRun: python maintenance_scripts/generate_skill_manifest.py "
        "(and bump the 'Bundle build:' line in radiant_llm_skills/SKILL.md to match) before committing."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
