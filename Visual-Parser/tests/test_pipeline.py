from visual_parser import pipeline
from visual_parser.config import ParserConfig


def test_ollama_warm_up_deferred_until_after_nougat_releases_gpu(monkeypatch, tmp_path):
    """Regression test: loading a local Ollama vision model must happen AFTER
    Nougat (Step 1) has run and released its GPU memory, not before. Real
    hardware testing found the warm-up call originally ran before Nougat even
    started, forcing Nougat to compete for whatever VRAM was left instead of
    having the GPU to itself first and releasing it afterward."""
    call_order = []

    fake_pdf = str(tmp_path / "doc.pdf")
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [fake_pdf])

    def fake_nougat_initializer(model_name):
        call_order.append("nougat_initializer")
        return ("fake_processor", "fake_model", "cpu")

    def fake_nougat_extract(**kwargs):
        call_order.append("nougat_extract")
        return ("summary", ["doc.pdf"], [], 5)

    monkeypatch.setattr("visual_parser.nougat_engine.NougatInitializer", fake_nougat_initializer)
    monkeypatch.setattr("visual_parser.text_extractor.nougat_extract_pdfs", fake_nougat_extract)

    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: call_order.append("ollama_warm_up"),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")

    monkeypatch.setattr(
        pipeline, "extract_pdf_metadata",
        lambda **kwargs: call_order.append("metadata_extraction") or {},
    )
    monkeypatch.setattr(
        pipeline, "describe_figures_for_new_pdfs",
        lambda **kwargs: call_order.append("figure_description"),
    )
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",  # explicit -- skips auto-selection
    )

    pipeline.run_pipeline(config)

    assert "nougat_initializer" in call_order and "ollama_warm_up" in call_order
    assert call_order.index("nougat_initializer") < call_order.index("ollama_warm_up"), (
        "Ollama's model load must happen AFTER Nougat starts, not before"
    )
    assert call_order.index("nougat_extract") < call_order.index("ollama_warm_up"), (
        "Ollama's model load must happen AFTER Nougat finishes, not before"
    )
    assert call_order.index("ollama_warm_up") < call_order.index("metadata_extraction")
    assert call_order.index("ollama_warm_up") < call_order.index("figure_description")


def test_ollama_warm_up_not_deferred_for_lightweight_text_mode(monkeypatch, tmp_path):
    """Lightweight text extraction never touches the GPU, so there's no
    Nougat-vs-Ollama contention to defer for -- warm-up should happen
    immediately, before metadata extraction, same as before this fix."""
    call_order = []

    fake_pdf = str(tmp_path / "doc.pdf")
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [fake_pdf])
    monkeypatch.setattr(
        "visual_parser.text_extractor.lightweight_extract_pdfs",
        lambda **kwargs: ("summary", ["doc.pdf"], [], 5),
    )
    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: call_order.append("ollama_warm_up"),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")
    monkeypatch.setattr(
        pipeline, "extract_pdf_metadata",
        lambda **kwargs: call_order.append("metadata_extraction") or {},
    )
    monkeypatch.setattr(pipeline, "describe_figures_for_new_pdfs", lambda **kwargs: None)
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="lightweight",
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",
    )

    pipeline.run_pipeline(config)

    assert call_order == ["ollama_warm_up", "metadata_extraction"]


def test_ollama_never_contacted_when_nothing_to_do(monkeypatch, tmp_path):
    """Regression test: a no-op run (no new PDFs) must stay a true no-op for
    --vision-provider ollama too, same as it already is for gpt/gemini --
    must not contact Ollama or load a model just to then do nothing with it."""
    monkeypatch.setattr(pipeline, "find_new_pdfs", lambda input_dir, rebuild: [])

    def fail_if_called(*a, **k):
        raise AssertionError("should not be called on a no-op run")

    monkeypatch.setattr("visual_parser.ollama_local.select_best_vision_model", fail_if_called)
    monkeypatch.setattr("visual_parser.ollama_local.warm_up_model", fail_if_called)

    config = ParserConfig(
        input_dir=str(tmp_path),
        text_mode="nougat",
        vision_provider="ollama",
        # no ollama_vision_model -- would normally trigger select_best_vision_model()
    )

    summary = pipeline.run_pipeline(config)
    assert summary["new_pdfs_found"] == 0


def test_ollama_never_contacted_when_nothing_to_do_skip_text(monkeypatch, tmp_path):
    def fail_if_called(*a, **k):
        raise AssertionError("should not be called on a no-op run")

    monkeypatch.setattr("visual_parser.ollama_local.select_best_vision_model", fail_if_called)
    monkeypatch.setattr("visual_parser.ollama_local.warm_up_model", fail_if_called)

    config = ParserConfig(
        input_dir=str(tmp_path),  # empty directory -- no PDFs at all
        skip_text=True,
        vision_provider="ollama",
    )

    pipeline.run_pipeline(config)


def test_ollama_warm_up_not_deferred_for_skip_text(monkeypatch, tmp_path):
    """--skip-text never runs Nougat at all, so there's nothing to defer for."""
    call_order = []
    fake_pdf = tmp_path / "doc.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake")

    monkeypatch.setattr(
        "visual_parser.ollama_local.warm_up_model",
        lambda model_name: call_order.append("ollama_warm_up"),
    )
    monkeypatch.setattr("visual_parser.ollama_local.get_loaded_model_gpu_status", lambda model_name: None)
    monkeypatch.setattr("visual_parser.ollama_local.describe_gpu_status", lambda status: "unknown")
    monkeypatch.setattr(
        pipeline, "extract_pdf_metadata",
        lambda **kwargs: call_order.append("metadata_extraction") or {},
    )
    monkeypatch.setattr(pipeline, "describe_figures_for_new_pdfs", lambda **kwargs: None)
    monkeypatch.setattr(pipeline, "mark_as_processed", lambda *a, **k: None)

    config = ParserConfig(
        input_dir=str(tmp_path),
        skip_text=True,
        vision_provider="ollama",
        ollama_vision_model="qwen3.6:35b-128k",
    )

    pipeline.run_pipeline(config)

    assert call_order == ["ollama_warm_up", "metadata_extraction"]
