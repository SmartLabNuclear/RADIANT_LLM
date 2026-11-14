"""
Visual-Parser is Apache-2.0. These tests keep copyleft PDF and string-matching
libraries (PyMuPDF/MuPDF: AGPL; python-Levenshtein/Levenshtein: GPL) from coming
back, in code or in the declared dependencies.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORBIDDEN_IMPORT = re.compile(r"^\s*(?:import|from)\s+(?:fitz|pymupdf|pymupdf4llm|Levenshtein)\b", re.MULTILINE)
FORBIDDEN_NAME = re.compile(r"pymupdf|levenshtein", re.IGNORECASE)


def _python_files():
    yield from (ROOT / "visual_parser").rglob("*.py")
    yield from (ROOT / "tests").rglob("*.py")


def test_no_copyleft_imports_in_code_or_tests():
    offenders = [str(p.relative_to(ROOT)) for p in _python_files() if FORBIDDEN_IMPORT.search(p.read_text(encoding="utf-8"))]
    assert offenders == []


def test_declared_dependencies_exclude_copyleft_packages():
    for name in ("pyproject.toml", "requirements.txt", "developer-scripts/docker-constraints.txt"):
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
            requirement = line.split("#", 1)[0]
            assert not FORBIDDEN_NAME.search(requirement), f"{name}: {line.strip()}"


def test_dockerfile_installs_no_mupdf_and_starts_from_a_clean_base():
    text = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    code = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("#"))
    assert not re.search(r"libmupdf|mupdf", code, re.IGNORECASE)
    assert re.search(r"^FROM python:", code, re.MULTILINE)
    assert "visual-parser-0.1.0" not in code
