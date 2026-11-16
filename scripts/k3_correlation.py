"""K3: are model errors correlated? (informational; with 20 tasks this is anecdotal)

For each pair of runs (A, B) over the tasks both completed (sample 0 by default):
  P(B wrong | A wrong)   wrong = not 'correct' (silent or loud)
  same-wrong count       tasks where both produced a valid but wrong output and the outputs are identical
Usage:  .venv/bin/python scripts/k3_correlation.py results/<run_a> results/<run_b> [...] [--sample N]
"""

import itertools
import json
import sys
from pathlib import Path


def load(run: Path, sample: int) -> dict[str, dict]:
    recs = [
        json.loads(line) for line in (run / "scores.jsonl").read_text().splitlines() if line.strip()
    ]
    return {r["task_id"]: r for r in recs if r["sample"] == sample}


def main(argv: list[str]) -> None:
    sample = 0
    if "--sample" in argv:
        i = argv.index("--sample")
        sample = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2 :]
    runs = {Path(a).name: load(Path(a), sample) for a in argv}
    for (na, a), (nb, b) in itertools.permutations(runs.items(), 2):
        tasks = sorted(set(a) & set(b))
        a_wrong = [t for t in tasks if a[t]["class"] != "correct"]
        both = [t for t in a_wrong if b[t]["class"] != "correct"]
        both_silent = [t for t in both if a[t]["class"] == b[t]["class"] == "silent_error"]
        measurable = [
            t for t in both_silent if a[t].get("output_digest") and b[t].get("output_digest")
        ]
        same = [t for t in measurable if a[t]["output_digest"] == b[t]["output_digest"]]
        same_txt = f"{len(same)} of {len(measurable)} measurable" + (
            f" ({len(both_silent) - len(measurable)} both-silent tasks lack output digests, e.g. runs made before digests existed)"
            if len(measurable) < len(both_silent)
            else ""
        )
        p = f"{len(both)}/{len(a_wrong)}" if a_wrong else "n/a (A never wrong)"
        print(
            f"A={na}  B={nb}: tasks={len(tasks)}  A wrong={len(a_wrong)}  P(B wrong | A wrong)={p}  both wrong={len(both)}  same wrong output={same_txt}"
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1:])
