"""Add output digests to an existing run by re-running each sample's final saved script in the sandbox.

Run directories store every attempt's code (<task>/s<k>/code_<n>.py). Scripts are deterministic, so
re-running the last one reproduces the output; the class is recomputed and compared with the stored
class. Writes <run_dir>/scores.jsonl in place (original kept as scores.before_digests.jsonl) and
prints any sample whose recomputed class differs from the stored one.
Usage: .venv/bin/python scripts/rescore_digests.py results/<run_dir> [more run dirs]
"""

import json
import shutil
import sys
from pathlib import Path

from tare.run_task import run_and_score
from tare.tasks import load_task


def rescore(run: Path) -> None:
    src = run / "scores.jsonl"
    backup = run / "scores.before_digests.jsonl"
    if not backup.exists():
        shutil.copy(src, backup)
    out, changed = [], 0
    for line in backup.read_text().splitlines():
        rec = json.loads(line)
        sdir = run / rec["task_id"] / f"s{rec['sample']}"
        codes = sorted(sdir.glob("code_*.py"), key=lambda p: int(p.stem.split("_")[1]))
        if rec["class"] in ("escalated",) or not codes:
            rec.setdefault("output_digest", None)
            out.append(rec)
            continue
        score, _res = run_and_score(
            load_task(rec["task_id"]), codes[-1].read_text(), "python", timeout=120
        )
        rec["output_digest"] = score.to_dict().get("output_digest")
        rec["matches_reading"] = score.matches_reading
        if score.klass != rec["class"]:
            changed += 1
            print(
                f"  CLASS DIFFERS {rec['task_id']} s{rec['sample']}: stored {rec['class']} vs recomputed {score.klass}"
            )
        out.append(rec)
    src.write_text("".join(json.dumps(r) + "\n" for r in out))
    print(
        f"{run.name}: {len(out)} records, {sum(r.get('output_digest') is not None for r in out)} with digests, {changed} class differences"
    )


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        rescore(Path(arg))
