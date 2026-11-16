"""Build a model client from a config block."""

import typer

from tare.providers import AnthropicClient, FakeClient, OpenAICompatClient


def make_client(cfg: dict):
    if cfg["provider"] == "ollama":
        return OpenAICompatClient(cfg["model"])
    if cfg["provider"] == "anthropic":
        return AnthropicClient(cfg["model"], cfg.get("effort"))
    if cfg["provider"] == "fake":
        return FakeClient(lambda _m: "```python\nprint('fake')\n```")
    raise typer.BadParameter(f"unsupported provider {cfg['provider']!r}")
