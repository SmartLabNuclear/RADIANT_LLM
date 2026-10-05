from visual_parser.pdf_tracker import (
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
