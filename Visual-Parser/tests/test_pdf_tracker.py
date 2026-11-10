import os

from visual_parser.pdf_tracker import (
    find_new_pdfs,
    load_processed_pdfs,
    mark_as_processed,
    unmark_as_processed,
)


def test_unmark_removes_a_match(tmp_path):
    registry = tmp_path / "04_processed_pdfs.txt"
    mark_as_processed(str(registry), ["a.pdf", "b.pdf"])

    removed = unmark_as_processed(str(registry), ["a.pdf"])

    assert removed == 1
    assert load_processed_pdfs(str(registry)) == ["b.pdf"]


def test_unmark_is_case_sensitive(tmp_path):
    """Matches load_processed_pdfs/mark_as_processed's own convention --
    these are what actually govern registry contents."""
    registry = tmp_path / "04_processed_pdfs.txt"
    mark_as_processed(str(registry), ["Doc.PDF"])

    removed = unmark_as_processed(str(registry), ["doc.pdf"])

    assert removed == 0
    assert load_processed_pdfs(str(registry)) == ["Doc.PDF"]


def test_unmark_noop_on_missing_registry(tmp_path):
    registry = tmp_path / "04_processed_pdfs.txt"
    assert unmark_as_processed(str(registry), ["a.pdf"]) == 0
    assert not registry.exists()


def test_unmark_does_not_rewrite_when_nothing_matches(tmp_path, monkeypatch):
    registry = tmp_path / "04_processed_pdfs.txt"
    mark_as_processed(str(registry), ["a.pdf"])

    import visual_parser.pdf_tracker as pdf_tracker

    def fail_if_called(*a, **k):
        raise AssertionError("save_processed_pdfs should not be called when nothing matched")

    monkeypatch.setattr(pdf_tracker, "save_processed_pdfs", fail_if_called)

    removed = unmark_as_processed(str(registry), ["not-in-registry.pdf"])
    assert removed == 0


def test_find_new_pdfs_uses_explicit_registry_path_when_given(tmp_path):
    """Regression test for the input_dir/output_dir registry mismatch: when
    output_dir differs from input_dir, the registry actually lives in
    output_dir, so an explicit registry_path must be honored instead of the
    input_dir-joined default."""
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()
    output_dir.mkdir()
    (input_dir / "a.pdf").write_bytes(b"stub")

    real_registry = output_dir / "04_processed_pdfs.txt"
    mark_as_processed(str(real_registry), ["a.pdf"])

    new_pdfs = find_new_pdfs(str(input_dir), registry_path=str(real_registry))

    assert new_pdfs == []


def test_find_new_pdfs_default_registry_path_unchanged(tmp_path):
    """Backward compatibility: omitting registry_path must keep resolving the
    registry against input_dir, exactly as before -- this is what RADIANT-LLM
    and any other same-folder caller relies on."""
    input_dir = tmp_path / "in"
    input_dir.mkdir()
    (input_dir / "a.pdf").write_bytes(b"stub")

    registry_in_input_dir = input_dir / "04_processed_pdfs.txt"
    mark_as_processed(str(registry_in_input_dir), ["a.pdf"])

    new_pdfs = find_new_pdfs(str(input_dir))

    assert new_pdfs == []


def test_find_new_pdfs_rebuild_ignores_registry_path(tmp_path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()
    output_dir.mkdir()
    pdf_path = input_dir / "a.pdf"
    pdf_path.write_bytes(b"stub")

    real_registry = output_dir / "04_processed_pdfs.txt"
    mark_as_processed(str(real_registry), ["a.pdf"])

    new_pdfs = find_new_pdfs(str(input_dir), rebuild=True, registry_path=str(real_registry))

    assert new_pdfs == [str(pdf_path)]
