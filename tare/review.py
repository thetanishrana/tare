"""Reviewer v2 (E8c): parse the reviewer's JSON and apply the escalation rule in code.

Rule (fixed in docs/09_DECISIONS.md, 2026-11-04): escalate if any listed choice has `spec_settles`
false and `changes_output` not "no". A reply that cannot be parsed escalates (fail safe, as for the
adjudicator): handing the case to a human never silently passes a point.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


@dataclass
class ReviewDecision:
    escalate: bool
    question: str | None
    choices: list[dict] = field(default_factory=list)
    parsed: bool = True


def parse_review_v2(text: str) -> ReviewDecision:
    m = _OBJECT.search(text)
    try:
        obj = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        obj = None
    if not isinstance(obj, dict) or not isinstance(obj.get("choices"), list):
        return ReviewDecision(
            True, "The reviewer reply could not be parsed: " + text[:200], [], False
        )
    open_points = [
        c
        for c in obj["choices"]
        if isinstance(c, dict)
        and c.get("spec_settles") is not True
        and str(c.get("changes_output", "unknown")).lower() != "no"
    ]
    if not open_points:
        return ReviewDecision(False, None, obj["choices"])
    first = open_points[0]
    question = str(
        first.get("question") or first.get("choice") or "An assumption is not settled by the spec."
    )
    return ReviewDecision(True, question, obj["choices"])
