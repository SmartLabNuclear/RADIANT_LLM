import pytest

from visual_parser.config import ParserConfig

# Model names confirmed dead against the live catalog and fixed in 2.1.1 --
# see vision_llm.py/model_catalog.py for the same set.
DEAD_MODEL_NAMES = {"gemini-3-pro-preview", "gemini-1.5-pro", "gpt-5.3-chat-latest"}


def test_defaults_are_not_dead_models():
    """Regression test for the dead-default-model bug fixed in 2.1.1."""
    config = ParserConfig(input_dir=".")
    assert config.gpt_vision_model not in DEAD_MODEL_NAMES
    assert config.gemini_vision_model not in DEAD_MODEL_NAMES
    assert config.gpt_vision_model == "gpt-5.4"
    assert config.gemini_vision_model == "gemini-3.8-flash"


def test_from_env_defaults_are_not_dead_models(monkeypatch):
    monkeypatch.delenv("VISUAL_PARSER_GPT_VISION_MODEL", raising=False)
    monkeypatch.delenv("VISUAL_PARSER_GEMINI_VISION_MODEL", raising=False)
    config = ParserConfig.from_env()
    assert config.gpt_vision_model not in DEAD_MODEL_NAMES
    assert config.gemini_vision_model not in DEAD_MODEL_NAMES


def test_from_env_reads_overrides(monkeypatch):
    monkeypatch.setenv("VISUAL_PARSER_CHUNK_SIZE", "777")
    monkeypatch.setenv("VISUAL_PARSER_REBUILD", "true")
    monkeypatch.setenv("VISUAL_PARSER_SKIP_TEXT", "false")
    config = ParserConfig.from_env()
    assert config.chunk_size == 777
    assert config.rebuild is True
    assert config.skip_text is False


def test_effective_output_dir_falls_back_to_input_dir():
    config = ParserConfig(input_dir="/some/input", output_dir="")
    assert config.effective_output_dir() == "/some/input"


def test_effective_output_dir_uses_explicit_output_dir():
    config = ParserConfig(input_dir="/some/input", output_dir="/some/output")
    assert config.effective_output_dir() == "/some/output"


def test_validate_requires_input_dir():
    config = ParserConfig(input_dir="")
    with pytest.raises(ValueError, match="input_dir must be set"):
        config.validate()


def test_validate_requires_existing_input_dir(tmp_path):
    missing = tmp_path / "does_not_exist"
    config = ParserConfig(input_dir=str(missing))
    with pytest.raises(ValueError, match="does not exist"):
        config.validate()


def test_validate_rejects_bad_text_mode(tmp_path):
    config = ParserConfig(input_dir=str(tmp_path), text_mode="bogus")
    with pytest.raises(ValueError, match="text_mode"):
        config.validate()


def test_validate_rejects_bad_vision_provider(tmp_path):
    config = ParserConfig(input_dir=str(tmp_path), vision_provider="bogus")
    with pytest.raises(ValueError, match="vision_provider"):
        config.validate()


def test_validate_requires_openai_key_for_gpt(tmp_path):
    config = ParserConfig(input_dir=str(tmp_path), vision_provider="gpt", openai_api_key="")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        config.validate()


def test_validate_requires_gemini_key_for_gemini(tmp_path):
    config = ParserConfig(
        input_dir=str(tmp_path), vision_provider="gemini", gemini_api_key="", openai_api_key="unused"
    )
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        config.validate()


def test_validate_passes_with_gpt_key(tmp_path):
    config = ParserConfig(input_dir=str(tmp_path), vision_provider="gpt", openai_api_key="sk-test")
    config.validate()  # should not raise
