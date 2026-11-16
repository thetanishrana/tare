"""Tabulate E8b: reviewer ask rates and the programmer-or-reviewer pipeline rates.
.venv/bin/python scripts/e8_review_report.py results/e8b/<reviewer>/reviews.jsonl [more]
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

from tare.tasks import ROOT, load_task

for path in map(Path, sys.argv[1:]):
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    print(f"== reviewer {path.parent.name}: {len(rows)} reviews")
    print(
        "programmer      | own v4 ask amb/clear | reviewer ask amb/clear (reviewed) | pipeline ask amb/clear"
    )
    for prog in ("haiku55", "sonnet55", "qwen3coder30b"):
        scores = [
            json.loads(x)
            for x in (ROOT / "results/e8" / prog / "v4/scores.jsonl").read_text().splitlines()
        ]
        n = defaultdict(int)
        own = defaultdict(int)
        for s in scores:
            k = "amb" if load_task(s["task_id"]).ambiguous else "clear"
            n[k] += 1
            own[k] += s["class"] == "escalated"
        rev = defaultdict(int)
        rev_n = defaultdict(int)
        for r in (r for r in rows if r["programmer"] == prog):
            k = "amb" if r["ambiguous"] else "clear"
            rev_n[k] += 1
            rev[k] += r["asked"]
        print(
            f"{prog:15s} | {own['amb']}/{n['amb']} {own['clear']}/{n['clear']} | "
            f"{rev['amb']}/{rev_n['amb']} {rev['clear']}/{rev_n['clear']} | "
            f"{own['amb'] + rev['amb']}/{n['amb']} {own['clear'] + rev['clear']}/{n['clear']}"
        )
