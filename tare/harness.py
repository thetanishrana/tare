"""Double-programming harness: two independent programmers, a comparator, an adjudicator.

    run_pair(task, client_a, client_b, ...) -> HarnessResult   (no answer key involved)
    score_harness(task, result)             -> Score           (post hoc, against the hidden oracle)

Decisions: `accepted` (outputs agree, or the adjudicator picked a side), `escalated` (a programmer
asked, the adjudicator or the rule escalated, or the assumption check raised a point) and `loud`
(a programmer produced no valid output). The assumption check is optional (`assumption_check`):
none, or a reviewer that reads both programmers' ASSUMPTIONS lists when their outputs agree, aimed
at an unstated choice both made the same way. See docs/09_DECISIONS.md (2026-10-28, E8b) for what a
single-prompt local reviewer achieved; it is a hypothesis to test, not a validated step.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from tare.adjudicate import Verdict, adjudicate
from tare.compare import CompareResult, compare_frames
from tare.programmer.agent import ESCALATED, OK, ProgramResult, program_task
from tare.prompts import build_review_messages, build_review_messages_v2, extract_escalation
from tare.providers.base import ModelClient
from tare.review import parse_review_v2
from tare.score import LOUD, Score, score_output
from tare.tasks import BUNDLES_DIR, Task

ACCEPTED, ESCALATE, FAILED = "accepted", "escalated", "loud"


@dataclass
class HarnessResult:
    task_id: str
    decision: str  # accepted | escalated | loud
    source: str | None  # agree | A | B | None
    output: pd.DataFrame | None
    question: str | None
    reason: str | None
    a: ProgramResult
    b: ProgramResult
    compare: CompareResult | None = None
    verdict: Verdict | None = None


def _assumption_check(
    spec: str,
    a: ProgramResult,
    b: ProgramResult,
    client: ModelClient,
    version: str = "v1",
    **params,
):
    lists = "\n".join(
        f"Programmer {n}:\n{(r.assumptions or '(none listed)').strip()}"
        for n, r in (("A", a), ("B", b))
    )
    if version == "v2":
        comp = client.complete(build_review_messages_v2(spec, lists), **params)
        decision = parse_review_v2(comp.text)
        return decision.question if decision.escalate else None
    comp = client.complete(build_review_messages(spec, lists), **params)
    return extract_escalation(comp.text)


def run_pair(
    task: Task,
    client_a: ModelClient,
    client_b: ModelClient,
    adjudicator: ModelClient | None = None,
    reviewer: ModelClient | None = None,
    language_a: str = "python",
    language_b: str = "python",
    prompt_version: str = "k2-v4",
    max_repairs: int = 2,
    params: dict[str, Any] | None = None,
    adjudicator_params: dict[str, Any] | None = None,
    reviewer_params: dict[str, Any] | None = None,
    reviewer_version: str = "v1",
) -> HarnessResult:
    """`adjudicator=None` is the rule policy (always escalate on disagreement); `reviewer=None`
    disables the assumption check."""
    a = program_task(task, client_a, language_a, prompt_version, max_repairs, params)
    b = program_task(task, client_b, language_b, prompt_version, max_repairs, params)
    return decide_pair(
        task, a, b, adjudicator, reviewer, adjudicator_params, reviewer_params, reviewer_version
    )


def decide_pair(
    task: Task,
    a: ProgramResult,
    b: ProgramResult,
    adjudicator: ModelClient | None = None,
    reviewer: ModelClient | None = None,
    adjudicator_params: dict[str, Any] | None = None,
    reviewer_params: dict[str, Any] | None = None,
    reviewer_version: str = "v1",
) -> HarnessResult:
    """The decision stage on two finished programmer results, so it can be replayed with another
    adjudicator or reviewer without running the programmers again."""

    def done(decision, source=None, out=None, q=None, why=None, cmp=None, verdict=None):
        return HarnessResult(task.id, decision, source, out, q, why, a, b, cmp, verdict)

    for r in (a, b):
        if r.status == ESCALATED:
            return done(ESCALATE, q=r.question, why="a programmer asked")
    if a.status != OK or b.status != OK:
        return done(FAILED, why="a programmer produced no valid output")
    assert a.output is not None and b.output is not None
    cmp = compare_frames(a.output, b.output, task.keys, task.target_vars, task.columns)
    spec = (BUNDLES_DIR / task.id / "spec.md").read_text()
    if cmp.agree:
        if reviewer is not None:
            q = _assumption_check(spec, a, b, reviewer, reviewer_version, **(reviewer_params or {}))
            if q:
                return done(ESCALATE, q=q, why="assumption check", cmp=cmp)
        return done(ACCEPTED, "agree", a.output, cmp=cmp)
    if adjudicator is None:
        return done(ESCALATE, why="outputs disagree (rule policy)", cmp=cmp)
    v = adjudicate(
        spec,
        a.code or "",
        b.code or "",
        a.assumptions,
        b.assumptions,
        cmp,
        adjudicator,
        **(adjudicator_params or {}),
    )
    if v.verdict == "escalate":
        return done(ESCALATE, q=v.question, why=v.reason, cmp=cmp, verdict=v)
    return done(
        ACCEPTED,
        v.verdict,
        a.output if v.verdict == "A" else b.output,
        why=v.reason,
        cmp=cmp,
        verdict=v,
    )


def score_harness(task: Task, result: HarnessResult) -> Score:
    """Classify a harness result against the hidden oracle. Escalations are their own class."""
    if result.decision == ESCALATE:
        return Score(task.id, "escalated")
    if result.decision == FAILED or result.output is None:
        return Score(task.id, LOUD, [result.reason or "no output"])
    with tempfile.TemporaryDirectory(prefix="tare-score-") as tmp:
        path = Path(tmp) / "result.parquet"
        result.output.to_parquet(path, index=False)
        return score_output(task, path)
