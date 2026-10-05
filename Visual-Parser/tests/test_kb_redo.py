import json

from visual_parser.kb_redo import KB_JSONL_FILENAMES, REGISTRY_FILENAMES, redo_entries
from visual_parser.pdf_tracker import load_processed_pdfs, mark_as_processed


def _write_rows(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_removes_only_matching_rows_across_all_kb_files(tmp_path):
    for filename in KB_JSONL_FILENAMES:
        _write_rows(
            tmp_path / filename,
            [{"source": "a.pdf", "x": 1}, {"source": "b.pdf", "x": 2}, {"source": "a.pdf", "x": 3}],
        )

    result = redo_entries(str(tmp_path), ["a.pdf"])

    assert result["totals"]["rows_removed"] == 2 * len(KB_JSONL_FILENAMES)
    for filename in KB_JSONL_FILENAMES:
        rows = [json.loads(l) for l in (tmp_path / filename).read_text(encoding="utf-8").splitlines() if l.strip()]
        assert rows == [{"source": "b.pdf", "x": 2}]
    assert result["cleared"] == ["a.pdf"]
    assert result["not_found"] == []


def test_backup_created_once_not_again_on_second_call(tmp_path):
    path = tmp_path / "02_visuals_kb.jsonl"
    _write_rows(path, [{"source": "a.pdf"}])
    backup_path = tmp_path / "02_visuals_kb_backup_before_redo.jsonl"

    redo_entries(str(tmp_path), ["a.pdf"])
    assert backup_path.exists()
    first_backup_content = backup_path.read_text(encoding="utf-8")

    # Re-seed the file and call again -- backup must NOT be overwritten.
    _write_rows(path, [{"source": "c.pdf"}])
    redo_entries(str(tmp_path), ["c.pdf"])
    assert backup_path.read_text(encoding="utf-8") == first_backup_content


def test_not_found_separates_typo_from_real_name(tmp_path):
    _write_rows(tmp_path / "02_visuals_kb.jsonl", [{"source": "real.pdf"}])

    result = redo_entries(str(tmp_path), ["real.pdf", "typo.pdf"])

    assert result["cleared"] == ["real.pdf"]
    assert result["not_found"] == ["typo.pdf"]


def test_registries_get_entries_stripped(tmp_path):
    for filename in REGISTRY_FILENAMES:
        mark_as_processed(str(tmp_path / filename), ["a.pdf", "b.png"])

    result = redo_entries(str(tmp_path), ["a.pdf"])

    for filename in REGISTRY_FILENAMES:
        assert load_processed_pdfs(str(tmp_path / filename)) == ["b.png"]
    assert result["totals"]["registry_entries_removed"] == len(REGISTRY_FILENAMES)
    assert "a.pdf" in result["cleared"]


def test_missing_files_handled_gracefully(tmp_path):
    """No KB files, no registries at all -- must not crash."""
    result = redo_entries(str(tmp_path), ["ghost.pdf"])
    assert result["cleared"] == []
    assert result["not_found"] == ["ghost.pdf"]
    assert result["totals"] == {"rows_removed": 0, "registry_entries_removed": 0}


def test_matches_by_basename_path_stripped(tmp_path):
    """Both the requested name and the on-disk basename should be
    path-stripped before comparison -- a full path passed to --redo should
    still match a bare basename stored as 'source'."""
    _write_rows(tmp_path / "02_visuals_kb.jsonl", [{"source": "a.pdf"}])

    result = redo_entries(str(tmp_path), [r"C:\some\other\dir\a.pdf"])

    assert result["cleared"] == ["a.pdf"]
    rows = [
        json.loads(l) for l in (tmp_path / "02_visuals_kb.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    assert rows == []
