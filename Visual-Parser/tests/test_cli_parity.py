"""
cli.py and cli_main.py are two independent copies of the same argument parser
and main() -- cli_main.py exists only because cli.py's unicode arrows crash
Windows consoles using the cp1252 codepage. Any flag added, renamed, or
re-defaulted in one must be mirrored in the other by hand; nothing enforces
that at import time. These tests catch drift between them directly, instead
of relying on someone noticing by eye.
"""

from pathlib import Path

import pytest

from visual_parser import cli, cli_main

MODULES = {"cli": cli, "cli_main": cli_main}


def _actions_by_dest(parser):
    return {a.dest: a for a in parser._actions if a.dest != "help"}


def test_cli_and_cli_main_have_identical_flag_structure():
    actions1 = _actions_by_dest(cli._build_arg_parser())
    actions2 = _actions_by_dest(cli_main._build_arg_parser())

    assert set(actions1.keys()) == set(actions2.keys())

    for dest in actions1:
        a1, a2 = actions1[dest], actions2[dest]
        assert a1.default == a2.default, f"--{dest}: default mismatch ({a1.default!r} vs {a2.default!r})"
        assert a1.choices == a2.choices, f"--{dest}: choices mismatch ({a1.choices!r} vs {a2.choices!r})"
        assert a1.required == a2.required, f"--{dest}: required mismatch"
        assert a1.option_strings == a2.option_strings, f"--{dest}: flag spelling mismatch"


def test_help_text_image_mentions_match():
    """cli.py and cli_main.py deliberately use different unicode-vs-ASCII
    characters in help text (that's the whole reason cli_main.py exists --
    see its module docstring), so help strings aren't expected to be
    byte-identical, and the structural parity test above doesn't compare
    them at all. But one file's help text documenting a real capability
    (e.g. standalone-image support) that the other omits entirely is a real
    content drift, not a cosmetic one -- this is a regression test for
    exactly that: --input-dir's help text in cli.py forgot to mention images
    when --skip-images was added to both files' flag sets."""
    actions1 = _actions_by_dest(cli._build_arg_parser())
    actions2 = _actions_by_dest(cli_main._build_arg_parser())

    for dest in actions1:
        if dest not in actions2:
            continue
        mentions1 = "image" in (actions1[dest].help or "").lower()
        mentions2 = "image" in (actions2[dest].help or "").lower()
        assert mentions1 == mentions2, (
            f"--{dest}: one file's help text mentions images, the other doesn't "
            f"(cli={mentions1}, cli_main={mentions2})"
        )


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_missing_input_dir_errors_unless_list_models(module_name):
    module = MODULES[module_name]
    with pytest.raises(SystemExit):
        module.main([])


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_main_resolves_default_vision_model_per_provider(module_name, monkeypatch, tmp_path):
    module = MODULES[module_name]
    captured = {}

    def fake_run_pipeline(config):
        captured["config"] = config
        return {}

    monkeypatch.setattr("visual_parser.pipeline.run_pipeline", fake_run_pipeline)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.delenv("PORTKEY_API_KEY", raising=False)
    monkeypatch.delenv("VISUAL_PARSER_FORCE_PORTKEY", raising=False)

    rc = module.main(["--input-dir", str(tmp_path)])
    assert rc == 0
    assert captured["config"].gpt_vision_model == "gpt-5.4"

    rc = module.main(["--input-dir", str(tmp_path), "--vision-provider", "gemini"])
    assert rc == 0
    assert captured["config"].gemini_vision_model == "gemini-3.8-flash"


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_main_respects_explicit_vision_model_override(module_name, monkeypatch, tmp_path):
    module = MODULES[module_name]
    captured = {}

    def fake_run_pipeline(config):
        captured["config"] = config
        return {}

    monkeypatch.setattr("visual_parser.pipeline.run_pipeline", fake_run_pipeline)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    module.main(["--input-dir", str(tmp_path), "--vision-model", "gpt-4o"])
    assert captured["config"].gpt_vision_model == "gpt-4o"


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_vision_model_stays_empty_for_ollama_with_no_override(module_name, monkeypatch, tmp_path):
    """Regression test: unlike gpt/gemini, 'ollama' must NOT get a hardcoded
    default vision model -- leaving it empty is what triggers VRAM-aware
    auto-selection in pipeline.py. Mocks select_best_vision_model so this
    test doesn't touch a real Ollama instance."""
    module = MODULES[module_name]
    captured = {}

    def fake_run_pipeline(config):
        captured["config"] = config
        return {}

    monkeypatch.setattr("visual_parser.pipeline.run_pipeline", fake_run_pipeline)
    monkeypatch.setattr("visual_parser.ollama_local.select_best_vision_model", lambda: "llava:13b")

    rc = module.main(["--input-dir", str(tmp_path), "--vision-provider", "ollama"])
    assert rc == 0
    assert captured["config"].ollama_vision_model == ""  # empty -- auto-selection was used
    assert captured["config"].vision_provider == "ollama"


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_vision_model_override_respected_for_ollama(module_name, monkeypatch, tmp_path):
    module = MODULES[module_name]
    captured = {}

    def fake_run_pipeline(config):
        captured["config"] = config
        return {}

    monkeypatch.setattr("visual_parser.pipeline.run_pipeline", fake_run_pipeline)

    rc = module.main([
        "--input-dir", str(tmp_path), "--vision-provider", "ollama", "--vision-model", "qwen2.5-vl:32b",
    ])
    assert rc == 0
    assert captured["config"].ollama_vision_model == "qwen2.5-vl:32b"


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_vision_context_pages_flag_reaches_config(module_name, monkeypatch, tmp_path):
    module = MODULES[module_name]
    captured = {}

    def fake_run_pipeline(config):
        captured["config"] = config
        return {}

    monkeypatch.setattr("visual_parser.pipeline.run_pipeline", fake_run_pipeline)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    module.main(["--input-dir", str(tmp_path), "--vision-context-pages", "1"])
    assert captured["config"].vision_context_pages == 1


@pytest.mark.parametrize("module_name", sorted(MODULES))
def test_main_returns_1_on_ollama_runtime_error(module_name, monkeypatch, tmp_path):
    """A RuntimeError from auto-selection (or the vision call itself) should
    print a clean [ERROR] message and return 1, not an unhandled traceback."""
    module = MODULES[module_name]

    def raising_run_pipeline(config):
        raise RuntimeError("No vision-capable Ollama models are pulled.")

    monkeypatch.setattr("visual_parser.pipeline.run_pipeline", raising_run_pipeline)

    rc = module.main(["--input-dir", str(tmp_path), "--vision-provider", "ollama"])
    assert rc == 1


def test_cli_main_returns_2_when_pipeline_reports_failures(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "visual_parser.pipeline.run_pipeline",
        lambda config: {"failed_basenames": ["broken.pdf"]},
    )
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.delenv("PORTKEY_API_KEY", raising=False)
    monkeypatch.delenv("VISUAL_PARSER_FORCE_PORTKEY", raising=False)

    rc = cli_main.main(["--input-dir", str(tmp_path)])
    assert rc == 2, "cli_main.main() should return 2 when the pipeline reports failed PDFs"


def test_cli_py_main_is_unreachable_from_any_real_entry_point():
    """cli.py's own main()/_build_arg_parser() are never actually invoked in
    the shipped package -- every real entry point calls cli_main.main
    directly. Only cli._print_available_models() is live (imported by
    cli_main.py for --list-models). This test reads the actual wiring rather
    than asserting something trivially true, so it breaks loudly if that
    ever changes -- which is also why the exit-code divergence between
    cli.main() and cli_main.main() (see the test above) was flagged for a
    decision instead of silently "fixed" to match: fixing dead code isn't
    the same as fixing a bug a user can hit."""
    import re

    repo_root = Path(__file__).resolve().parent.parent

    pyproject_text = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'visual-parser\s*=\s*"([^"]+)"', pyproject_text)
    assert match is not None, "visual-parser script entry not found in pyproject.toml"
    assert match.group(1) == "visual_parser.cli_main:main"

    dunder_main_text = (repo_root / "visual_parser" / "__main__.py").read_text(encoding="utf-8")
    assert "from visual_parser.cli_main import main" in dunder_main_text
    assert "from visual_parser.cli import main" not in dunder_main_text

    top_level_script_text = (repo_root / "visual-parser.py").read_text(encoding="utf-8")
    assert "from visual_parser.cli_main import main" in top_level_script_text
    assert "from visual_parser.cli import main" not in top_level_script_text
