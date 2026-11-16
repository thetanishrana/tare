from types import SimpleNamespace

import pytest

from tare.pricing import cost_usd
from tare.providers import anthropic_client
from tare.providers.anthropic_client import AnthropicClient


def _fake_response(text="```python\nprint(1)\n```", stop="end_turn"):
    usage = SimpleNamespace(
        input_tokens=100, output_tokens=50, cache_creation_input_tokens=0, cache_read_input_tokens=0
    )
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        usage=usage,
        model="claude-sonnet-5-5",
        id="msg_1",
        stop_reason=stop,
    )


def test_missing_key_refuses(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(anthropic_client, "load_dotenv", lambda *_a, **_k: None)
    with pytest.raises(RuntimeError, match="missing"):
        AnthropicClient("claude-sonnet-5-5")


def test_request_shape_and_no_sampling_params(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    c = AnthropicClient("claude-sonnet-5-5")
    seen = {}

    def create(**kw):
        seen.update(kw)
        return _fake_response()

    c._client = SimpleNamespace(messages=SimpleNamespace(create=create))
    comp = c.complete(
        [{"role": "system", "content": "sys"}, {"role": "user", "content": "hi"}],
        max_tokens=1000,
        temperature=0.2,
    )
    assert seen["system"] == "sys" and seen["messages"] == [{"role": "user", "content": "hi"}]
    assert "temperature" not in seen and "thinking" not in seen and "output_config" not in seen
    assert (
        comp.text.startswith("```python")
        and comp.usage.input_tokens == 100
        and comp.stop_reason == "end_turn"
    )


def test_effort_goes_in_output_config(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    c = AnthropicClient("claude-haiku-5-5", effort="low")
    seen = {}
    c._client = SimpleNamespace(
        messages=SimpleNamespace(create=lambda **kw: (seen.update(kw), _fake_response())[1])
    )
    c.complete([{"role": "user", "content": "hi"}])
    assert seen["output_config"] == {"effort": "low"}


def test_cost_usd():
    assert cost_usd("claude-sonnet-5-5", 1_000_000, 100_000) == pytest.approx(3.0)
    assert cost_usd("claude-haiku-5-5", 1_000_000, 1_000_000) == pytest.approx(0.6)
    assert cost_usd("qwen3-coder:30b", 10, 10) == 0.0
    assert cost_usd("unknown-model", 1, 1) is None
