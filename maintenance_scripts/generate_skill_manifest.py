#!/usr/bin/env python3
"""Developer CLI — hash all bundled skill files and write MANIFEST.json.

Run before every release after editing any bundled skill file:
  python maintenance_scripts/generate_skill_manifest.py

Then commit both the changed skill file and the updated MANIFEST.json.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

MANIFEST_EXTENSIONS = frozenset(
    {".md", ".txt", ".yaml", ".yml", ".py", ".tex", ".i", ".toml", ".cfg"}
)


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate_manifest(bundled_root: Path) -> dict:
    manifest = {}
    for path in sorted(bundled_root.rglob("*")):
        if path.is_file() and path.suffix.lower() in MANIFEST_EXTENSIONS:
            rel = path.relative_to(bundled_root).as_posix()
            manifest[rel] = _file_hash(path)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate MANIFEST.json for RADIANT-LLM bundled skill files."
    )
    parser.add_argument(
        "--root",
        default=None,
        help=(
            "Path to the bundled skills root. "
            "Defaults to radiant_llm_skills/ next to the project root."
        ),
    )
    args = parser.parse_args()

    if args.root:
        bundled_root = Path(args.root).resolve()
    else:
        project_root = Path(__file__).resolve().parent.parent
        bundled_root = project_root / "radiant_llm_skills"

    if not bundled_root.exists():
        print(f"ERROR: bundled root not found: {bundled_root}", file=sys.stderr)
        return 1

    manifest = generate_manifest(bundled_root)
    manifest_path = bundled_root / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(manifest)} entries to {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
