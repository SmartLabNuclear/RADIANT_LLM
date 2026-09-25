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
