"""Adjudicator: called when two programmers disagree. It never sees the oracle or answer keys.

Input: the spec, both programs and their assumption lists, and the structured diff between the two
outputs. Output: a verdict (A, B, or escalate with one precise question for a human).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from tare.compare import CompareResult
from tare.providers.base import ModelClient

ADJUDICATOR_PROMPT = """Two programmers independently wrote code for the same clinical trial dataset derivation, and their outputs disagree. Decide which output follows the spec, or whether the spec leaves open a point that only the study team can settle.

# Spec

{spec}

# Programmer A

Assumptions listed:
{assumptions_a}

Code:
```
{code_a}
```

# Programmer B

Assumptions listed:
{assumptions_b}

Code:
```
{code_b}
```

# How the outputs differ

{diff}

Reply with one JSON object and nothing else:
{{"verdict": "A" | "B" | "escalate", "reason": "<one or two sentences>", "question": "<if escalate: one precise question a human could answer, else null>"}}

Choose "A" or "B" only if the spec itself settles the point. If both readings are defensible, choose "escalate".
"""

MAX_CODE_CHARS = 6000


@dataclass
class Verdict:
    verdict: str  # A | B | escalate
    reason: str
    question: str | None


def describe_diff(cmp: CompareResult) -> str:
    lines = [
        f"rows in A: {cmp.n_left}, rows in B: {cmp.n_right}",
        f"keys only in A: {cmp.missing_keys}, keys only in B: {cmp.extra_keys}",
        f"records that differ: {cmp.mismatched_records}; per variable: {cmp.mismatches}",
        "sample of differing records (A = `__a`, B = `__b`):",
    ]
    lines += [json.dumps(s) for s in cmp.sample[:10]]
    return "\n".join(lines)


_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def parse_verdict(text: str) -> Verdict:
    """Parse the adjudicator's JSON. Anything malformed becomes an escalation: failing safe means
    handing the case to a human, never silently picking a side."""
    m = _OBJECT.search(text)
    try:
        obj = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        obj = {}
    verdict = str(obj.get("verdict", "")).strip()
    reason = str(obj.get("reason") or "")
    question = obj.get("question") or None
    if verdict not in ("A", "B", "escalate"):
        return Verdict("escalate", "unparseable adjudicator reply: " + text[:200], None)
    if verdict == "escalate" and not question:
        return Verdict("escalate", reason or "escalated without a question", None)
    return Verdict(verdict, reason, str(question) if question else None)


def adjudicate(
    spec: str,
    code_a: str,
    code_b: str,
    assumptions_a: str | None,
    assumptions_b: str | None,
    cmp: CompareResult,
    client: ModelClient,
    **params,
) -> Verdict:
    prompt = ADJUDICATOR_PROMPT.format(
        spec=spec.strip(),
        assumptions_a=(assumptions_a or "(none listed)").strip(),
        assumptions_b=(assumptions_b or "(none listed)").strip(),
        code_a=code_a[:MAX_CODE_CHARS],
        code_b=code_b[:MAX_CODE_CHARS],
        diff=describe_diff(cmp),
    )
    comp = client.complete([{"role": "user", "content": prompt}], **params)
    return parse_verdict(comp.text)
