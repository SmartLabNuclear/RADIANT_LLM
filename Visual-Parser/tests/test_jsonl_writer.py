import json

from visual_parser.jsonl_writer import append_to_jsonl, atomic_rewrite_jsonl


def test_append_returns_true_on_success(tmp_path):
    path = tmp_path / "out.jsonl"
    assert append_to_jsonl(str(path), [{"a": 1}]) is True
    assert json.loads(path.read_text(encoding="utf-8").strip()) == {"a": 1}


def test_append_returns_false_when_new_data_is_not_a_list(tmp_path):
    path = tmp_path / "out.jsonl"
    assert append_to_jsonl(str(path), {"a": 1}) is False  # type: ignore[arg-type]
    assert not path.exists()


def test_append_returns_false_on_filesystem_error(tmp_path, monkeypatch):
    """Simulates a disk-full/permission-style failure: open() itself raises."""
    path = tmp_path / "out.jsonl"

    def raising_open(*a, **k):
        raise OSError("disk full")

    monkeypatch.setattr("builtins.open", raising_open)
    assert append_to_jsonl(str(path), [{"a": 1}]) is False


# ---------------------------------------------------------------------------
# atomic_rewrite_jsonl
# ---------------------------------------------------------------------------

def _write_lines(path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_atomic_rewrite_keeps_and_drops_rows(tmp_path):
    path = tmp_path / "kb.jsonl"
    _write_lines(path, [{"source": "a.pdf"}, {"source": "b.pdf"}, {"source": "a.pdf"}])

    stats = atomic_rewrite_jsonl(str(path), lambda row: row["source"] != "a.pdf")

    assert stats == {"removed": 2, "kept": 1, "malformed": 0}
    remaining = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert remaining == [{"source": "b.pdf"}]


def test_atomic_rewrite_counts_malformed_lines(tmp_path):
    path = tmp_path / "kb.jsonl"
    path.write_text('{"source": "a.pdf"}\nnot json\n{"source": "b.pdf"}\n', encoding="utf-8")

    stats = atomic_rewrite_jsonl(str(path), lambda row: True)

    assert stats == {"removed": 0, "kept": 2, "malformed": 1}


def test_atomic_rewrite_missing_file_is_a_graceful_noop(tmp_path):
    path = tmp_path / "does_not_exist.jsonl"
    stats = atomic_rewrite_jsonl(str(path), lambda row: True)
    assert stats == {"removed": 0, "kept": 0, "malformed": 0}
    assert not path.exists()  # not created by this call
