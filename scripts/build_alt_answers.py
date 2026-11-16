"""Build answer keys for the alternative defensible readings of ambiguous tasks.

Each reading has a reference solution in benchmark/reference/alt/<task>__<reading>.py, run in the
sandbox on the task bundle; its output becomes data/answers/<task>__<reading>.parquet. Also reports how
many records each reading differs from the oracle and from the other readings, because a reading that
changes nothing is not a real alternative.
    .venv/bin/python scripts/build_alt_answers.py [task_id ...]
"""

import shutil
import sys
import tempfile
from pathlib import Path

import pandas as pd

from tare.compare import compare_frames
from tare.sandbox.runner import run_in_sandbox
from tare.score import contract_violations
from tare.tasks import ANSWERS_DIR, BENCHMARK, BUNDLES_DIR, alt_answer_path, load_all_tasks

want = set(sys.argv[1:])
bad = 0
for t in load_all_tasks():
    if not t.readings or (want and t.id not in want):
        continue
    oracle = pd.read_parquet(ANSWERS_DIR / f"{t.id}.parquet")
    outs = {}
    for r in t.readings:
        code = (BENCHMARK / "reference" / "alt" / f"{t.id}__{r['id']}.py").read_text()
        with tempfile.TemporaryDirectory(prefix="tare-alt-") as tmp:
            wd = Path(tmp)
            shutil.copytree(BUNDLES_DIR / t.id / "inputs", wd / "inputs")
            (wd / "out").mkdir()
            (wd / "code.py").write_text(code)
            res = run_in_sandbox(wd, "python", timeout=120)
            path = wd / "out" / "result.parquet"
            if not res.ok or not path.exists():
                print(f"{t.id}__{r['id']}: FAILED to run: {res.stderr[-300:]}")
                bad += 1
                continue
            df = pd.read_parquet(path)
            problems = contract_violations(path, t.contract(), df)
            if problems:
                print(f"{t.id}__{r['id']}: contract problems {problems}")
                bad += 1
                continue
        df[t.keys + t.target_vars].to_parquet(alt_answer_path(t.id, r["id"]), index=False)
        outs[r["id"]] = df
        c = compare_frames(oracle, df, t.keys, t.target_vars, t.columns)
        n_diff = (
            c.mismatched_records + c.missing_keys + c.extra_keys
        )  # row-set tasks differ in keys
        flag = "" if n_diff else "  <-- IDENTICAL to oracle, not an alternative"
        bad += not n_diff
        print(f"{t.id:20s} {r['id']:24s} differs from oracle on {n_diff}/{c.n_left}{flag}")
    ids = list(outs)
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            c = compare_frames(outs[a], outs[b], t.keys, t.target_vars, t.columns)
            if not (c.mismatched_records or c.missing_keys or c.extra_keys):
                print(f"{t.id}: readings {a} and {b} are identical")
                bad += 1
sys.exit(1 if bad else 0)
