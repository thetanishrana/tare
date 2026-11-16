"""Run one piece of code against one task bundle and score it: bundle -> sandbox -> scorer."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from tare.sandbox.runner import COMMANDS, SandboxResult, run_in_sandbox
from tare.score import Score, score_output
from tare.tasks import BUNDLES_DIR, Task


def run_and_score(
    task: Task, code: str, language: str, timeout: int = 120
) -> tuple[Score, SandboxResult]:
    code_file = COMMANDS[language][0]
    with tempfile.TemporaryDirectory(prefix="tare-run-") as tmp:
        wd = Path(tmp)
        shutil.copytree(BUNDLES_DIR / task.id / "inputs", wd / "inputs")
        (wd / "out").mkdir()
        (wd / code_file).write_text(code)
        res = run_in_sandbox(wd, language, timeout=timeout)
        score = score_output(task, wd / "out" / "result.parquet")
    return score, res
