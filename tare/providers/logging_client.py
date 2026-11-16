"""Wrap a model client so every call is appended to calls.jsonl (messages, response, usage, role)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tare.providers.base import Completion, ModelClient


class LoggingClient:
    def __init__(self, inner: ModelClient, calls_log: Path, role: str, context: dict[str, Any]):
        self.inner, self.calls_log, self.role = inner, calls_log, role
        self.context = context  # mutable: the runner sets task_id and sample before each pair
        self.provider, self.model = inner.provider, inner.model

    def complete(self, messages: list[dict[str, str]], **params: Any) -> Completion:
        comp = self.inner.complete(messages, **params)
        with self.calls_log.open("a") as f:
            f.write(
                json.dumps(
                    {
                        **self.context,
                        "role": self.role,
                        "model": comp.model,
                        "params": comp.params or params,
                        "messages": messages,
                        "response": comp.text,
                        "usage": vars(comp.usage),
                        "stop_reason": comp.stop_reason,
                        "latency_s": comp.latency_s,
                    }
                )
                + "\n"
            )
        return comp

    def identity(self) -> dict[str, Any]:
        return self.inner.identity()
