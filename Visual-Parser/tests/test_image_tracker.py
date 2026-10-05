from visual_parser import image_tracker
from visual_parser.image_tracker import find_new_images


def test_finds_images_by_extension(tmp_path):
    (tmp_path / "a.png").write_bytes(b"fake")
    (tmp_path / "b.JPG").write_bytes(b"fake")  # case-insensitive
    (tmp_path / "c.pdf").write_bytes(b"fake")  # not an image -- excluded
    (tmp_path / "d.txt").write_bytes(b"fake")  # not an image -- excluded

    registry_path = str(tmp_path / "parsed_images.txt")
    found = find_new_images(str(tmp_path), registry_path)

    basenames = {__import__("os").path.basename(p) for p in found}
    assert basenames == {"a.png", "b.JPG"}


def test_already_processed_images_are_excluded(tmp_path):
    (tmp_path / "a.png").write_bytes(b"fake")
    (tmp_path / "b.png").write_bytes(b"fake")

    registry_path = tmp_path / "parsed_images.txt"
    registry_path.write_text("a.png\n", encoding="utf-8")

    found = find_new_images(str(tmp_path), str(registry_path))
    assert [p for p in found if p.endswith("a.png")] == []
    assert any(p.endswith("b.png") for p in found)


def test_rebuild_ignores_registry(tmp_path):
    (tmp_path / "a.png").write_bytes(b"fake")

    registry_path = tmp_path / "parsed_images.txt"
    registry_path.write_text("a.png\n", encoding="utf-8")

    found = find_new_images(str(tmp_path), str(registry_path), rebuild=True)
    assert any(p.endswith("a.png") for p in found)


def test_no_images_returns_empty_list(tmp_path):
    (tmp_path / "doc.pdf").write_bytes(b"fake")
    found = find_new_images(str(tmp_path), str(tmp_path / "parsed_images.txt"))
    assert found == []


def test_load_processed_pdfs_is_monkeypatchable_at_module_level(tmp_path, monkeypatch):
    """Regression test: load_processed_pdfs must be imported at module level
    (not inside find_new_images' own body), or monkeypatch.setattr(
    image_tracker, "load_processed_pdfs", ...) -- the idiomatic way tests in
    this file stub registry-loading without touching the filesystem --
    would silently have no effect, since a function-local import re-resolves
    the real pdf_tracker.load_processed_pdfs fresh on every call."""
    (tmp_path / "a.png").write_bytes(b"fake")

    monkeypatch.setattr(image_tracker, "load_processed_pdfs", lambda registry_path: ["a.png"])

    found = find_new_images(str(tmp_path), str(tmp_path / "parsed_images.txt"))
    assert found == []  # "a.png" reported processed by the stub, correctly excluded


def test_registry_path_is_explicit_not_joined_against_input_dir(tmp_path):
    """Deliberate deviation from find_new_pdfs(): the registry lives wherever
    the caller points it (e.g. output_dir), not auto-joined against input_dir
    -- this sidesteps the pre-existing PDF-side input_dir/output_dir registry
    mismatch bug."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    (input_dir / "a.png").write_bytes(b"fake")

    registry_in_output = output_dir / "parsed_images.txt"
    registry_in_output.write_text("a.png\n", encoding="utf-8")

    # Registry says "a.png" is done, and it's correctly excluded even though
    # the registry file lives in a completely different directory than the
    # images themselves.
    found = find_new_images(str(input_dir), str(registry_in_output))
    assert found == []
