import logging

import pytest
import requests

from visual_parser import ollama_local


@pytest.fixture(autouse=True)
def _reset_base_url_cache(monkeypatch):
    monkeypatch.setattr(ollama_local, "_resolved_base_url_cache", None)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)


def test_resolve_base_url_env_var_used_verbatim(monkeypatch):
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://my-ollama-host:11434/")
    assert ollama_local.resolve_ollama_base_url() == "http://my-ollama-host:11434"


def test_resolve_base_url_probes_localhost_first(monkeypatch):
    def fake_get(url, timeout):
        if url == "http://localhost:11434/api/tags":
            return type("Resp", (), {"raise_for_status": lambda self: None})()
        raise requests.RequestException("should not reach this host")

    monkeypatch.setattr(requests, "get", fake_get)
    assert ollama_local.resolve_ollama_base_url() == "http://localhost:11434/v1"


def test_resolve_base_url_falls_back_to_host_docker_internal(monkeypatch):
    def fake_get(url, timeout):
        if url == "http://localhost:11434/api/tags":
            raise requests.RequestException("unreachable")
        if url == "http://host.docker.internal:11434/api/tags":
            return type("Resp", (), {"raise_for_status": lambda self: None})()
        raise requests.RequestException("unexpected host")

    monkeypatch.setattr(requests, "get", fake_get)
    assert ollama_local.resolve_ollama_base_url() == "http://host.docker.internal:11434/v1"


def test_resolve_base_url_returns_none_when_unreachable(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, timeout: (_ for _ in ()).throw(requests.RequestException()))
    assert ollama_local.resolve_ollama_base_url() is None


class _FakeResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def raise_for_status(self):
        pass

    def json(self):
        return self._json_data


def test_list_ollama_models_parses_and_sorts(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    fake_data = {
        "models": [
            {
                "name": "llava:13b",
                "size": 8_000_000_000,
                "modified_at": "2026-01-01T00:00:00Z",
                "details": {"parameter_size": "13B", "quantization_level": "Q4_K_M"},
            },
            {
                "name": "qwen2.5-vl:32b",
                "size": 20_000_000_000,
                "modified_at": "2026-05-01T00:00:00Z",
                "details": {"parameter_size": "32B", "quantization_level": "Q4_K_M"},
            },
        ]
    }
    monkeypatch.setattr(requests, "get", lambda url, timeout: _FakeResponse(fake_data))

    models = ollama_local.list_ollama_models()
    assert [m.id for m in models] == ["qwen2.5-vl:32b", "llava:13b"]  # newest first
    assert models[0].size_bytes == 20_000_000_000
    assert "32B" in models[0].label


def test_list_ollama_models_returns_empty_when_unreachable(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: None)
    assert ollama_local.list_ollama_models() == []


def test_list_ollama_models_returns_empty_on_request_exception(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    monkeypatch.setattr(requests, "get", lambda url, timeout: (_ for _ in ()).throw(requests.RequestException()))
    assert ollama_local.list_ollama_models() == []


def test_get_model_capabilities_reads_field(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    monkeypatch.setattr(
        requests, "post",
        lambda url, json, timeout: _FakeResponse({"capabilities": ["completion", "vision"]}),
    )
    assert ollama_local.get_model_capabilities("qwen2.5-vl:32b") == ["completion", "vision"]


def test_get_model_capabilities_missing_field_returns_empty(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    monkeypatch.setattr(requests, "post", lambda url, json, timeout: _FakeResponse({}))
    assert ollama_local.get_model_capabilities("some-model") == []


def test_looks_vision_capable_name_heuristic():
    assert ollama_local._looks_vision_capable("llava:13b") is True
    assert ollama_local._looks_vision_capable("qwen2.5-vl:32b") is True
    assert ollama_local._looks_vision_capable("qwen2.5:32b") is False
    assert ollama_local._looks_vision_capable("llama3.1:70b") is False


def test_list_vision_capable_models_filters(monkeypatch):
    models = [
        ollama_local.OllamaModel("qwen2.5:32b", "qwen2.5:32b", 20_000_000_000, "Q4_K_M", "2026-01-01"),
        ollama_local.OllamaModel("llava:13b", "llava:13b", 8_000_000_000, "Q4_K_M", "2026-01-01"),
        ollama_local.OllamaModel("some-vision-model:7b", "some-vision-model:7b", 4_000_000_000, "Q4_K_M", "2026-01-01"),
    ]
    monkeypatch.setattr(ollama_local, "list_ollama_models", lambda: models)

    def fake_capabilities(name, timeout=3.0):
        if name == "some-vision-model:7b":
            return ["completion", "vision"]
        return []

    monkeypatch.setattr(ollama_local, "get_model_capabilities", fake_capabilities)

    result = {m.id for m in ollama_local.list_vision_capable_models()}
    # llava:13b -- caught by name heuristic; some-vision-model:7b -- caught by capabilities field
    assert result == {"llava:13b", "some-vision-model:7b"}
    assert "qwen2.5:32b" not in result


def test_get_free_vram_bytes_no_gpu(monkeypatch):
    import torch
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    assert ollama_local.get_free_vram_bytes() is None


def test_get_free_vram_bytes_with_gpu(monkeypatch):
    import torch
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "mem_get_info", lambda: (42_000_000_000, 96_000_000_000))
    assert ollama_local.get_free_vram_bytes() == 42_000_000_000


def _fake_vision_models():
    return [
        ollama_local.OllamaModel("llava:7b", "llava:7b", 4_000_000_000, "Q4_K_M", "2026-01-01"),
        ollama_local.OllamaModel("qwen2.5-vl:32b", "qwen2.5-vl:32b", 20_000_000_000, "Q4_K_M", "2026-01-01"),
        ollama_local.OllamaModel("qwen2.5-vl:72b", "qwen2.5-vl:72b", 45_000_000_000, "Q4_K_M", "2026-01-01"),
    ]


def test_select_best_vision_model_picks_largest_that_fits(monkeypatch):
    monkeypatch.setattr(ollama_local, "list_vision_capable_models", _fake_vision_models)
    monkeypatch.setattr(ollama_local, "get_free_vram_bytes", lambda: 42_000_000_000)  # 42 GB free

    # budget = 42e9 * 0.85 = 35.7e9 -- 72b (45e9) doesn't fit, 32b (20e9) does
    assert ollama_local.select_best_vision_model() == "qwen2.5-vl:32b"


def test_select_best_vision_model_falls_back_to_cpu_when_no_gpu_visible(monkeypatch, caplog, capsys):
    """No GPU at all is a legitimate CPU-only setup -- should fall back to
    the smallest pulled vision-capable model with a warning, not raise.
    Must also be printed directly, not just logged -- logger.warning() is
    silently dropped at the default --log-level ERROR (WARNING < ERROR), so
    a log-only message would never reach the user in the common case."""
    monkeypatch.setattr(ollama_local, "list_vision_capable_models", _fake_vision_models)
    monkeypatch.setattr(ollama_local, "get_free_vram_bytes", lambda: None)

    with caplog.at_level(logging.WARNING):
        result = ollama_local.select_best_vision_model()

    assert result == "llava:7b"  # smallest of _fake_vision_models()
    assert "CPU-only" in caplog.text
    assert "llava:7b" in caplog.text

    printed = capsys.readouterr().out
    assert "CPU-only" in printed
    assert "llava:7b" in printed


def test_select_best_vision_model_raises_when_none_pulled(monkeypatch):
    monkeypatch.setattr(ollama_local, "list_vision_capable_models", lambda: [])
    monkeypatch.setattr(ollama_local, "list_ollama_models", lambda: [])

    with pytest.raises(RuntimeError, match="ollama pull"):
        ollama_local.select_best_vision_model()


def test_select_best_vision_model_raises_when_none_vision_capable(monkeypatch):
    monkeypatch.setattr(ollama_local, "list_vision_capable_models", lambda: [])
    monkeypatch.setattr(
        ollama_local, "list_ollama_models",
        lambda: [ollama_local.OllamaModel("llama3.1:70b", "llama3.1:70b", 40_000_000_000, "Q4_K_M", "2026-01-01")],
    )

    with pytest.raises(RuntimeError, match="vision-capable"):
        ollama_local.select_best_vision_model()


def test_warm_up_model_posts_minimal_request(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    captured = {}

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        return _FakeResponse({})

    monkeypatch.setattr(requests, "post", fake_post)
    ollama_local.warm_up_model("llava:13b")
    assert captured["url"] == "http://localhost:11434/v1/chat/completions"
    assert captured["json"]["model"] == "llava:13b"


def test_warm_up_model_swallows_request_exception(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    monkeypatch.setattr(requests, "post", lambda url, json, timeout: (_ for _ in ()).throw(requests.RequestException()))
    ollama_local.warm_up_model("llava:13b")  # should not raise


def test_warm_up_model_noop_when_unreachable(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: None)

    def fail_if_called(*a, **k):
        raise AssertionError("should not attempt a request when unreachable")

    monkeypatch.setattr(requests, "post", fail_if_called)
    ollama_local.warm_up_model("llava:13b")  # should not raise or call requests.post


def test_get_loaded_model_gpu_status_finds_matching_model(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    fake_data = {"models": [{"name": "qwen3.6:35b-128k", "size": 23_410_895_745, "size_vram": 2_610_241_207}]}
    monkeypatch.setattr(requests, "get", lambda url, timeout: _FakeResponse(fake_data))

    status = ollama_local.get_loaded_model_gpu_status("qwen3.6:35b-128k")
    assert status == {"size_bytes": 23_410_895_745, "size_vram_bytes": 2_610_241_207}


def test_get_loaded_model_gpu_status_matches_untagged_name_against_implicit_latest(monkeypatch):
    """Regression test: Ollama reports a pulled-without-tag model back as
    "name:latest" in /api/ps -- 'ollama pull llava' (the README's own
    example) followed by querying status for 'llava' must still match."""
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    fake_data = {"models": [{"name": "llava:latest", "size": 8_000_000_000, "size_vram": 8_000_000_000}]}
    monkeypatch.setattr(requests, "get", lambda url, timeout: _FakeResponse(fake_data))

    status = ollama_local.get_loaded_model_gpu_status("llava")
    assert status == {"size_bytes": 8_000_000_000, "size_vram_bytes": 8_000_000_000}


def test_get_loaded_model_gpu_status_returns_none_when_not_loaded(monkeypatch):
    monkeypatch.setattr(ollama_local, "resolve_ollama_base_url", lambda **kw: "http://localhost:11434/v1")
    monkeypatch.setattr(requests, "get", lambda url, timeout: _FakeResponse({"models": []}))
    assert ollama_local.get_loaded_model_gpu_status("llava:13b") is None


def test_describe_gpu_status_fully_on_gpu():
    status = {"size_bytes": 10_000_000_000, "size_vram_bytes": 10_000_000_000}
    assert "fully on GPU" in ollama_local.describe_gpu_status(status)


def test_describe_gpu_status_cpu_only():
    status = {"size_bytes": 10_000_000_000, "size_vram_bytes": 0}
    assert "CPU only" in ollama_local.describe_gpu_status(status)


def test_describe_gpu_status_partial_offload():
    status = {"size_bytes": 23_410_895_745, "size_vram_bytes": 2_610_241_207}
    result = ollama_local.describe_gpu_status(status)
    assert "partially on GPU" in result
    assert "2.6 GB" in result
    assert "23.4 GB" in result


def test_describe_gpu_status_unknown_when_not_loaded():
    assert "unknown" in ollama_local.describe_gpu_status(None)


def test_select_best_vision_model_raises_when_nothing_fits(monkeypatch):
    monkeypatch.setattr(ollama_local, "list_vision_capable_models", _fake_vision_models)
    monkeypatch.setattr(ollama_local, "get_free_vram_bytes", lambda: 1_000_000_000)  # 1 GB free -- nothing fits

    with pytest.raises(RuntimeError, match="llava:7b"):  # names the smallest as a hint
        ollama_local.select_best_vision_model()
