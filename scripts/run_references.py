"""Run every reference solution in the sandbox and score it against the hidden answer.

The reference solutions (benchmark/reference/) are my own independent implementations of each spec.
A task is well-posed only if its reference scores 'correct'. Run after building bundles:
    .venv/bin/python scripts/run_references.py [task_id ...]
"""

import json
import sys

from tare.run_task import run_and_score
from tare.tasks import BENCHMARK, load_all_tasks

want = set(sys.argv[1:])
rows = []
for t in load_all_tasks():
    if want and t.id not in want:
        continue
    code = (BENCHMARK / "reference" / f"{t.id}.py").read_text()
    score, res = run_and_score(t, code, "python")
    d = score.to_dict()
    print(
        f"{t.id:24s} {score.klass:13s} run_ok={res.ok} {res.seconds:4.1f}s",
        ""
        if score.klass == "correct"
        else json.dumps({k: d.get(k) for k in ("problems", "mismatches", "mismatched_records")}),
    )
    if not res.ok:
        print("   stderr:", res.stderr[-400:])
    elif score.klass != "correct" and d.get("sample"):
        for s in d["sample"][:4]:
            print("   ", s)
    rows.append(d)
print("correct:", sum(r["class"] == "correct" for r in rows), "of", len(rows))
