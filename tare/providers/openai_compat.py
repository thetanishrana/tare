"""OpenAI-compatible client: covers Ollama (http://localhost:11434/v1) and OpenAI."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from typing import Any

from openai import OpenAI

from tare.providers.base import Completion, Usage

OLLAMA_URL = os.environ.get("TARE_OLLAMA_URL", "http://localhost:11434")


class OpenAICompatClient:
    def __init__(
        self,
        model: str,
        base_url: str = OLLAMA_URL + "/v1",
        api_key: str = "ollama",
        provider: str = "ollama",
    ):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        self._client = OpenAI(base_url=base_url, api_key=api_key, timeout=900)

    def complete(self, messages: list[dict[str, str]], **params: Any) -> Completion:
        t0 = time.monotonic()
        r = self._client.chat.completions.create(model=self.model, messages=messages, **params)
        usage = Usage(
            input_tokens=getattr(r.usage, "prompt_tokens", 0) or 0,
            output_tokens=getattr(r.usage, "completion_tokens", 0) or 0,
        )
        return Completion(
            r.choices[0].message.content or "",
            usage,
            time.monotonic() - t0,
            self.model,
            params,
            r.model_dump(),
        )

    def identity(self) -> dict[str, Any]:
        info: dict[str, Any] = {"provider": self.provider, "model": self.model}
        if self.provider == "ollama":
            req = urllib.request.Request(
                OLLAMA_URL + "/api/show",
                data=json.dumps({"model": self.model}).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                show = json.load(resp)
            info["details"] = show.get("details")
            tags = json.load(urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=30))
            info["digest"] = next(
                (m["digest"] for m in tags["models"] if m["name"] == self.model), None
            )
        return info
