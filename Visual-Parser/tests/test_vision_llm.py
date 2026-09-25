import logging

import pytest

from visual_parser import vision_llm

DEAD_MODEL_NAMES = {"gemini-3-pro-preview", "gemini-1.5-pro", "gpt-5.3-chat-latest"}


def test_latest_model_constants_are_not_dead():
    assert vision_llm.LATEST_GPT_MODEL not in DEAD_MODEL_NAMES
    assert vision_llm.LATEST_GEMINI_MODEL not in DEAD_MODEL_NAMES
    assert vision_llm.LATEST_GEMINI_MODEL == "gemini-3.8-flash"


def test_no_hardcoded_dead_model_set_remains():
    """_GPT_NO_REASONING_MODELS only ever held 'gpt-5.3-chat-latest', which the
    generic '-chat-latest' suffix check already covers -- removed as dead
    weight when the model was pulled out. This guards against it (or a
    similar hardcoded dead-model set) creeping back in."""
    assert not hasattr(vision_llm, "_GPT_NO_REASONING_MODELS")


@pytest.mark.parametrize("model", ["gpt-5", "gpt-5.1", "gpt-5.2", "gpt-5.4", "gpt-5.5", "gpt-5.6", "gpt-6-luna"])
def test_supports_reasoning_effort_true_for_reasoning_family(model):
    assert vision_llm._supports_reasoning_effort(model) is True


@pytest.mark.parametrize("model", ["gpt-4o", "gpt-4.1", "gpt-4-turbo", "gpt-4"])
def test_supports_reasoning_effort_false_for_older_gpt(model):
    assert vision_llm._supports_reasoning_effort(model) is False


@pytest.mark.parametrize("model", ["gpt-5.3-chat-latest", "gpt-4o-chat-latest", "foo-chat-latest"])
def test_chat_latest_suffix_still_detected_after_dead_set_removal(model):
    """Regression test: removing the hardcoded gpt-5.3-chat-latest set must not
    change behavior, since the generic suffix check was already covering it."""
    assert vision_llm._supports_reasoning_effort(model) is False
    assert vision_llm._is_gpt5_chat_latest(model) is True


def test_normalize_reasoning_effort_known_model_allowed_value():
    assert vision_llm._normalize_reasoning_effort("gpt-5.4", "xhigh") == "xhigh"


def test_normalize_reasoning_effort_known_model_disallowed_value(caplog):
    with caplog.at_level(logging.WARNING):
        result = vision_llm._normalize_reasoning_effort("gpt-5", "xhigh")  # gpt-5 doesn't support xhigh
    assert result is None
    assert "Ignoring unsupported reasoning_effort" in caplog.text


def test_normalize_reasoning_effort_unrecognized_model_falls_back_to_default_set():
    # gpt-5.6 isn't in _GPT_REASONING_EFFORT_OPTIONS but IS reasoning-capable
    assert vision_llm._normalize_reasoning_effort("gpt-5.6", "medium") == "medium"


def test_normalize_reasoning_effort_none_input():
    assert vision_llm._normalize_reasoning_effort("gpt-5.4", None) is None


class _FakeResponse:
    def __init__(self, text):
        message = type("Msg", (), {"content": text})()
        choice = type("Choice", (), {"message": message})()
        self.choices = [choice]


class _FakeChatCompletions:
    def __init__(self):
        self.captured_kwargs = None

    def create(self, **kwargs):
        self.captured_kwargs = kwargs
        return _FakeResponse("described")


class _FakeOpenAIClient:
    def __init__(self, api_key, base_url):
        self.chat = type("Chat", (), {"completions": _FakeChatCompletions()})()


def _patch_openai_client(monkeypatch):
    monkeypatch.setattr(
        "visual_parser.openai_gateway.resolve_openai_connection",
        lambda: {"api_key": "sk-test", "base_url": None, "model_prefix": ""},
    )
    fake_client = _FakeOpenAIClient(api_key="sk-test", base_url=None)
    monkeypatch.setattr("openai.OpenAI", lambda api_key, base_url: fake_client)
    return fake_client


def test_call_vision_llm_gpt_uses_reasoning_effort_for_reasoning_model(monkeypatch):
    fake_client = _patch_openai_client(monkeypatch)
    result = vision_llm.call_vision_llm_gpt(
        images=[b"fake-png-bytes"],
        prompt="describe",
        api_key="sk-test",
        model="gpt-5.4",
        reasoning_effort="medium",
    )
    assert result == "described"
    kwargs = fake_client.chat.completions.captured_kwargs
    assert kwargs["reasoning_effort"] == "medium"
    assert "temperature" not in kwargs


def test_call_vision_llm_gpt_uses_temperature_for_chat_latest_model(monkeypatch):
    fake_client = _patch_openai_client(monkeypatch)
    vision_llm.call_vision_llm_gpt(
        images=[b"fake-png-bytes"],
        prompt="describe",
        api_key="sk-test",
        model="gpt-4o-chat-latest",
    )
    kwargs = fake_client.chat.completions.captured_kwargs
    assert kwargs["temperature"] == 1.0
    assert "reasoning_effort" not in kwargs


def test_call_vision_llm_gpt_uses_temperature_zero_for_older_model(monkeypatch):
    fake_client = _patch_openai_client(monkeypatch)
    vision_llm.call_vision_llm_gpt(
        images=[b"fake-png-bytes"],
        prompt="describe",
        api_key="sk-test",
        model="gpt-4o",
    )
    kwargs = fake_client.chat.completions.captured_kwargs
    assert kwargs["temperature"] == 0
    assert "reasoning_effort" not in kwargs
