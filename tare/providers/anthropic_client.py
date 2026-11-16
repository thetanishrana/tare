"""Anthropic Messages API client.

Notes (verified against the API docs, 2026-10-18):
  * Claude Sonnet 5.5 rejects non-default temperature/top_p/top_k, so sampling parameters are
    never sent; runs use the API defaults. Thinking is adaptive and effort defaults to the
    model's own default unless a config sets `effort`.
  * We do not enable server-side refusal fallbacks: a silent switch to another model would
    corrupt a per-model measurement. A refusal is recorded (stop_reason) and scores as a
    loud error (no code block).
  * Credentials come from ANTHROPIC_API_KEY (loaded from .env if present). The key is never logged.
"""

from __future__ import annotations

import os
import time
from typing import Any

import anthropic
from dotenv import load_dotenv

from tare.providers.base import Completion, Usage
from tare.tasks import ROOT


def key_status() -> str:
    """'set' or 'missing' - never the value."""
    load_dotenv(ROOT / ".env")
    return "set" if os.environ.get("ANTHROPIC_API_KEY") else "missing"


class AnthropicClient:
    provider = "anthropic"

    def __init__(self, model: str, effort: str | None = None):
        if key_status() != "set":
            raise RuntimeError("ANTHROPIC_API_KEY is missing (put it in .env)")
        self.model = model
        self.effort = effort
        self._client = anthropic.Anthropic()

    def complete(self, messages: list[dict[str, str]], **params: Any) -> Completion:
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        chat = [m for m in messages if m["role"] != "system"]
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": params.get("max_tokens", 16000),
            "messages": chat,
        }
        if system:
            kwargs["system"] = system
        if self.effort:
            kwargs["output_config"] = {"effort": self.effort}
        t0 = time.monotonic()
        r = self._client.messages.create(**kwargs)
        text = "".join(b.text for b in r.content if b.type == "text")
        u = r.usage
        usage = Usage(
            input_tokens=(u.input_tokens or 0)
            + (getattr(u, "cache_creation_input_tokens", 0) or 0)
            + (getattr(u, "cache_read_input_tokens", 0) or 0),
            output_tokens=u.output_tokens or 0,
            cached_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
        )
        sent = {k: v for k, v in kwargs.items() if k not in ("messages", "system")}
        return Completion(
            text, usage, time.monotonic() - t0, r.model, sent, {"id": r.id}, r.stop_reason
        )

    def identity(self) -> dict[str, Any]:
        return {
            "provider": "anthropic",
            "model": self.model,
            "effort": self.effort or "model default",
        }
