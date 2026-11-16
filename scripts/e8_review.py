"""E8b: run a reviewer over the logged k2-v4 assumption lists (docs/09_DECISIONS.md, 2026-10-28).

For each sample in results/e8/<programmer>/v4/scores.jsonl that has an assumptions list and was not
an escalation, the reviewer sees the task spec and the list and replies ESCALATE: <question> or
PROCEED. Writes results/e8b/<reviewer>/reviews.jsonl (one record per reviewed sample).
    .venv/bin/python scripts/e8_review.py <ollama|anthropic> <model> [programmer ...]
"""

import json
import sys

from tare.cli import make_client
from tare.pricing import cost_usd
from tare.prompts import build_review_messages, extract_escalation
from tare.tasks import BUNDLES_DIR, ROOT, load_task

provider, model = sys.argv[1], sys.argv[2]
programmers = sys.argv[3:] or ["haiku55", "sonnet55", "qwen3coder30b"]
client = make_client({"provider": provider, "model": model})
out_dir = ROOT / "results" / "e8b" / model.replace(":", "_")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "reviews.jsonl"
params = {"max_tokens": 4096 if provider == "ollama" else 1024}
if provider == "ollama":
    params["temperature"] = 0.2

done = set()
if out_file.exists():
    done = {
        (r["programmer"], r["task_id"], r["sample"])
        for r in map(json.loads, out_file.read_text().splitlines())
    }
for prog in programmers:
    src = ROOT / "results" / "e8" / prog / "v4" / "scores.jsonl"
    for line in src.read_text().splitlines():
        rec = json.loads(line)
        if rec["class"] == "escalated" or not rec.get("assumptions"):
            continue
        key = (prog, rec["task_id"], rec["sample"])
        if key in done:
            continue
        spec = (BUNDLES_DIR / rec["task_id"] / "spec.md").read_text()
        comp = client.complete(build_review_messages(spec, rec["assumptions"]), **params)
        question = extract_escalation(comp.text)
        row = {
            "programmer": prog,
            "task_id": rec["task_id"],
            "sample": rec["sample"],
            "ambiguous": load_task(rec["task_id"]).ambiguous,
            "programmer_class": rec["class"],
            "asked": question is not None,
            "question": question,
            "reply": comp.text if question is None else None,
            "cost_usd": cost_usd(client.model, comp.usage.input_tokens, comp.usage.output_tokens),
        }
        with out_file.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(prog, rec["task_id"], rec["sample"], "ASK" if row["asked"] else "proceed", flush=True)
