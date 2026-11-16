"""Fake provider: returns canned responses, for tests and dry runs at zero cost."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from tare.providers.base import Completion, Usage


class FakeClient:
    provider = "fake"

    def __init__(self, respond: Callable[[list[dict[str, str]]], str], model: str = "fake-1"):
        self.model = model
        self._respond = respond
        self.calls = 0

    def complete(self, messages: list[dict[str, str]], **params: Any) -> Completion:
        self.calls += 1
        text = self._respond(messages)
        n_in = sum(len(m["content"]) for m in messages) // 4
        return Completion(text, Usage(n_in, len(text) // 4), 0.0, self.model, params, None)

    def identity(self) -> dict[str, Any]:
        return {"provider": "fake", "model": self.model}
