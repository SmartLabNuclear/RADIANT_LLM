import pytest

from visual_parser import model_catalog


@pytest.mark.parametrize(
    "model_id,expected",
    [
        ("gpt-5.4", True),
        ("gpt-4o", True),
        ("gpt-6-luna", True),
        ("text-embedding-3-large", False),
        ("whisper-1", False),
        ("dall-e-3", False),
        ("tts-1", False),
        ("gpt-realtime", False),
        ("computer-use-preview", False),
        ("gpt-4-0613", False),  # dated snapshot suffix
        ("gpt-4.1-2025-04-14", False),  # dated snapshot suffix
    ],
)
def test_looks_chat_capable(model_id, expected):
    assert model_catalog._looks_chat_capable(model_id) is expected


def test_model_version_sort_key_orders_newer_first():
    ids = ["gpt-4o", "gpt-5.4", "gpt-4.1", "gpt-5"]
    ordered = sorted(ids, key=model_catalog._model_version_sort_key, reverse=True)
    assert ordered.index("gpt-5.4") < ordered.index("gpt-4o")
    assert ordered.index("gpt-5") < ordered.index("gpt-4.1")


class _FakeOpenAIModel:
    def __init__(self, id_, created=None):
        self.id = id_
        self.created = created


class _FakeModelsList:
    def __init__(self, models):
        self._models = models

    def list(self):
        return type("Resp", (), {"data": self._models})()


class _FakeOpenAIClient:
    def __init__(self, models):
        self.models = _FakeModelsList(models)


def test_list_openai_models_filters_excluded_ids(monkeypatch):
    fake_models = [
        _FakeOpenAIModel("gpt-5.4", created=100),
        _FakeOpenAIModel("gpt-6-astra", created=99),  # Responses-API-only, explicitly excluded
        _FakeOpenAIModel("o3-mini", created=98),  # o-series excluded
        _FakeOpenAIModel("gpt-3.5-turbo", created=97),  # two generations behind
        _FakeOpenAIModel("text-embedding-3-large", created=96),  # non-chat
        _FakeOpenAIModel("gpt-5.3-chat-latest", created=95),  # -chat-latest suffix
        _FakeOpenAIModel("codex-mini", created=94),  # codex excluded
    ]
    monkeypatch.setattr("openai.Client", lambda api_key, base_url: _FakeOpenAIClient(fake_models))

    result = model_catalog.list_openai_models("sk-test", force_refresh=True)

    assert "gpt-5.4" in result
    for excluded in ("gpt-6-astra", "o3-mini", "gpt-3.5-turbo", "text-embedding-3-large",
                     "gpt-5.3-chat-latest", "codex-mini"):
        assert excluded not in result


class _FakeGeminiModel:
    def __init__(self, name, methods):
        self.name = name
        self.supported_generation_methods = methods


def test_list_gemini_models_filters_non_content_and_omni(monkeypatch):
    fake_models = [
        _FakeGeminiModel("models/gemini-3.8-flash", ["generateContent"]),
        _FakeGeminiModel("models/embedding-001", ["embedContent"]),
        _FakeGeminiModel("models/gemini-omni-preview", ["generateContent"]),
    ]
    monkeypatch.setattr("google.generativeai.configure", lambda api_key: None)
    monkeypatch.setattr("google.generativeai.list_models", lambda: fake_models)

    result = model_catalog.list_gemini_models("fake-key", force_refresh=True)

    assert "gemini-3.8-flash" in result
    assert "embedding-001" not in result
    assert "gemini-omni-preview" not in result
