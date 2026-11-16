"""Rebuild programmer results from a logged pair run, so the decision stage can be rerun with another
adjudicator or reviewer without calling the programmers again.

The final response of each programmer for a task sample is re-parsed (escalation, code,
assumptions) and its code re-run in the sandbox; generated code is deterministic, so this
reproduces the original output. Everything comes from calls.jsonl; no answer key is involved.
"""

from __future__ import annotations

import json
from pathlib import Path

from tare.programmer.agent import ESCALATED, LOUD, OK, ProgramResult, execute
from tare.prompts import extract_assumptions, extract_code, extract_escalation
from tare.tasks import Task


def _entries(calls_log: Path) -> list[dict]:
    return [json.loads(line) for line in calls_log.read_text().splitlines()]


def programmer_from_log(
    task: Task, entries: list[dict], role: str, sample: int, language: str = "python"
) -> ProgramResult | None:
    mine = [
        e
        for e in entries
        if e["task_id"] == task.id and e["sample"] == sample and e["role"] == role
    ]
    if not mine:
        return None
    last = mine[-1]
    res = ProgramResult(
        task.id,
        last["model"],
        language,
        LOUD,
        attempts=len(mine),
        input_tokens=sum(e["usage"]["input_tokens"] for e in mine),
        output_tokens=sum(e["usage"]["output_tokens"] for e in mine),
        assumptions=extract_assumptions(last["response"]),
    )
    question = extract_escalation(last["response"])
    if question is not None:
        res.status, res.question = ESCALATED, question
        return res
    code = extract_code(last["response"], language)
    res.code = code
    if code is not None:
        _run, df, problems = execute(task, code, language)
        res.problems = problems
        if df is not None and not problems:
            res.status, res.output = OK, df
    return res


def programmers_from_log(
    task: Task,
    run_dir: Path,
    sample: int = 0,
    language_a: str = "python",
    language_b: str = "python",
) -> tuple[ProgramResult, ProgramResult] | None:
    entries = _entries(Path(run_dir) / "calls.jsonl")
    a = programmer_from_log(task, entries, "programmer_a", sample, language_a)
    b = programmer_from_log(task, entries, "programmer_b", sample, language_b)
    return (a, b) if a and b else None
