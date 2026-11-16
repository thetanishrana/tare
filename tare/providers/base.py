"""One interface for every model backend: ModelClient.complete(messages, **params) -> Completion."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0


@dataclass
class Completion:
    text: str
    usage: Usage
    latency_s: float
    model: str
    params: dict[str, Any] = field(default_factory=dict)
    raw: Any = None
    stop_reason: str | None = None


class ModelClient(Protocol):
    provider: str
    model: str

    def complete(self, messages: list[dict[str, str]], **params: Any) -> Completion: ...

    def identity(self) -> dict[str, Any]:
        """Facts that pin the model for reproducibility (id, digest where known)."""
        ...
