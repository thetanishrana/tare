"""API-equivalent cost from token counts and the list prices in configs/pricing.yaml."""

from __future__ import annotations

from functools import lru_cache

import yaml

from tare.tasks import ROOT


@lru_cache(maxsize=1)
def _prices() -> dict:
    return yaml.safe_load((ROOT / "configs" / "pricing.yaml").read_text())["models"]


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float | None:
    """Uncached, non-batch cost; None if the model has no price entry."""
    p = _prices().get(model)
    if p is None:
        return None
    return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
