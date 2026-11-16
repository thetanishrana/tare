"""One programmer: prompt -> code -> sandbox -> output, with repairs for loud errors.

Isolation by construction: this module never imports the scorer, the answer keys or the oracle, and
the model only ever sees its own stderr and the structural contract problems. The result carries
the output dataframe, so the harness can compare two programmers without any answer key.
"""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd

from tare.compare import contract_violations
from tare.prompts import (
    ESCALATION_VERSIONS,
    build_messages,
    build_repair_messages,
    extract_assumptions,
    extract_code,
    extract_escalation,
)
from tare.providers.base import ModelClient
from tare.sandbox.runner import COMMANDS, SandboxResult, run_in_sandbox
from tare.tasks import BUNDLES_DIR, Task

OK, LOUD, ESCALATED = "ok", "loud", "escalated"


@dataclass
class ProgramResult:
    task_id: str
    model: str
    language: str
    status: str  # ok | loud | escalated
    code: str | None = None
    output: pd.DataFrame | None = None
    question: str | None = None
    assumptions: str | None = None
    attempts: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    problems: list[str] = field(default_factory=list)


def _feedback(res: SandboxResult | None, problems: list[str], no_code: bool) -> str:
    if no_code:
        return "Your reply did not contain a fenced code block."
    parts = []
    if res is not None and not res.ok:
        status = "timed out" if res.timed_out else f"exit code {res.exit_code}"
        parts.append(f"The script failed ({status}).\nstderr (end):\n{res.stderr[-2500:]}")
    if problems:
        parts.append("Problems with the output file:\n- " + "\n- ".join(problems))
    return "\n\n".join(parts) or "The script produced no output file at /work/out/result.parquet."


def execute(
    task: Task, code: str, language: str, timeout: int = 120
) -> tuple[SandboxResult, pd.DataFrame | None, list[str]]:
    """Run code in the sandbox on the task's inputs; return the result, the output frame (if the run
    produced a readable output file) and the contract problems with it."""
    code_file = COMMANDS[language][0]
    with tempfile.TemporaryDirectory(prefix="tare-prog-") as tmp:
        wd = Path(tmp)
        shutil.copytree(BUNDLES_DIR / task.id / "inputs", wd / "inputs")
        (wd / "out").mkdir()
        (wd / code_file).write_text(code)
        res = run_in_sandbox(wd, language, timeout=timeout)
        path = wd / "out" / "result.parquet"
        if res.ok and path.exists():
            df = pd.read_parquet(path)
            return res, df, contract_violations(path, task.contract(), df)
    return res, None, []


def program_task(
    task: Task,
    client: ModelClient,
    language: str = "python",
    prompt_version: str = "k2-v4",
    max_repairs: int = 2,
    params: dict[str, Any] | None = None,
    timeout: int = 120,
) -> ProgramResult:
    params = params or {}
    messages = build_messages(task, language, prompt_version)
    res_out = ProgramResult(task.id, client.model, language, LOUD)
    for _attempt in range(max_repairs + 1):
        comp = client.complete(messages, **params)
        res_out.attempts += 1
        res_out.input_tokens += comp.usage.input_tokens
        res_out.output_tokens += comp.usage.output_tokens
        found = extract_assumptions(comp.text)
        if found:
            res_out.assumptions = found
        if prompt_version in ESCALATION_VERSIONS:
            question = extract_escalation(comp.text)
            if question is not None:
                res_out.status, res_out.question = ESCALATED, question
                return res_out
        code = extract_code(comp.text, language)
        res, problems, df = None, [], None
        if code is not None:
            res, df, problems = execute(task, code, language, timeout)
        res_out.code = code
        if code is not None and df is not None and not problems:
            res_out.status, res_out.output, res_out.problems = OK, df, []
            return res_out
        res_out.problems = problems
        messages = build_repair_messages(
            messages, code or "", language, _feedback(res, problems, code is None)
        )
    return res_out
