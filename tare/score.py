"""Score one output dataset against a task's hidden answer.

Classes (see docs/04_BENCHMARK_SPEC.md):
  correct       valid output, every target value matches the answer for every key
  silent error  valid output (contract satisfied, all keys present, none extra) with at least one
                wrong target value
  loud error    no output, unreadable output, or a contract violation (missing columns, wrong types,
                nulls or values outside the contract, duplicate/missing/extra keys)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow as pa

from tare.compare import CompareResult, compare_frames, contract_violations, output_digest
from tare.tasks import ANSWERS_DIR, Task, alt_answer_path

CORRECT, SILENT, LOUD = "correct", "silent_error", "loud_error"


@dataclass
class Score:
    task_id: str
    klass: str
    problems: list[str] = field(default_factory=list)
    compare: CompareResult | None = None
    digest: str | None = None
    matches_reading: str | None = None  # id of the defensible alternative reading matched

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "task_id": self.task_id,
            "class": self.klass,
            "problems": self.problems,
            "output_digest": self.digest,
            "matches_reading": self.matches_reading,
        }
        if self.compare:
            c = self.compare
            d.update(
                n_answer=c.n_left,
                n_output=c.n_right,
                mismatches=c.mismatches,
                mismatched_records=c.mismatched_records,
                mismatch_share=c.mismatched_records / max(1, c.n_left),
                sample=c.sample,
            )
        return d


def score_output(task: Task, output_path: Path, answer: pd.DataFrame | None = None) -> Score:
    if not output_path.exists():
        return Score(task.id, LOUD, ["no output file"])
    try:
        out = pd.read_parquet(output_path)
    except (OSError, ValueError, pa.ArrowException) as e:  # unreadable parquet
        return Score(task.id, LOUD, [f"unreadable output: {e}"])
    contract = task.contract()
    problems = contract_violations(output_path, contract, out)
    if problems:
        return Score(task.id, LOUD, problems)
    if answer is None:
        answer = pd.read_parquet(ANSWERS_DIR / f"{task.id}.parquet")
    cmp = compare_frames(answer, out, task.keys, task.target_vars, task.columns)
    # for tasks whose answer is a set of derived records, the row set is part of the answer: a
    # different set of keys is then a silent error (task field `rowset_is_target`), not a contract break
    if (cmp.missing_keys or cmp.extra_keys) and not task.raw.get("rowset_is_target"):
        probs = [f"{cmp.missing_keys} expected keys missing, {cmp.extra_keys} unexpected keys"]
        return Score(task.id, LOUD, probs, cmp)
    digest = output_digest(out, task.keys, task.target_vars, task.columns)
    score = Score(task.id, CORRECT if cmp.agree else SILENT, [], cmp, digest)
    if not cmp.agree:
        score.matches_reading = _matching_reading(task, out)
    return score


def _matching_reading(task: Task, out: pd.DataFrame) -> str | None:
    """A silent error that equals a stored defensible reading is still silent (the choice was not
    flagged), but it is recorded so the report can show "matches any defensible reading"."""
    for r in task.readings:
        path = alt_answer_path(task.id, r["id"])
        if path.exists():
            alt = pd.read_parquet(path)
            if compare_frames(alt, out, task.keys, task.target_vars, task.columns).agree:
                return r["id"]
    return None
