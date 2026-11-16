"""Build the write-up figures from the logged score records (no hand-typed numbers).

    .venv/bin/python scripts/make_figures.py        -> docs/figures/assumption_check.png

Figure: outcomes of the Claude pair on the 21 ambiguous tasks, three samples (H4, H4b and H4c), with the
assumption check off (replay of the same logged programmers) and on.
"""

import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    "check off": [
        "results/h4/replay_reviewer_off",
        "results/h4b/replay_reviewer_off",
        "results/h4c/replay_reviewer_off",
    ],
    "check on": ["results/h4/claude_pair", "results/h4b/claude_pair", "results/h4c/claude_pair"],
}
SURFACE, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
# categorical slots 1, 3, 2 of the reference palette (validated: all checks pass; the aqua contrast
# warning is covered by the visible counts in every segment)
STYLE = [
    ("escalated", "Escalated (asked a question)", "#2a78d6", "white"),
    ("correct", "Accepted, right reading by luck", "#1baf7a", INK),
    ("silent_error", "Accepted, wrong reading", "#eb6834", INK),
]


def load(dirs: list[str]) -> list[dict]:
    rows = []
    for d in dirs:
        rows += [json.loads(x) for x in (ROOT / d / "scores.jsonl").read_text().splitlines()]
    return rows


counts, clear = {}, {}
for label, dirs in RUNS.items():
    rows = load(dirs)
    counts[label] = Counter(r["class"] for r in rows if r["ambiguous"])
    clear[label] = Counter(r["class"] for r in rows if not r["ambiguous"])

fig, ax = plt.subplots(figsize=(9.2, 3.6), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
labels = list(RUNS)
for y, label in enumerate(reversed(labels)):
    left = 0
    for key, _, color, ink in STYLE:
        n = counts[label].get(key, 0)
        if n:
            ax.barh(y, n, left=left, height=0.52, color=color, edgecolor=SURFACE, linewidth=2)
            ax.text(
                left + n / 2,
                y,
                str(n),
                ha="center",
                va="center",
                color=ink,
                fontsize=11,
                weight="bold",
            )
        left += n
    total = sum(counts[label].values())
    ax.text(-0.6, y, f"{label}\n(n = {total})", ha="right", va="center", color=INK, fontsize=10)
ax.set_xlim(0, max(sum(c.values()) for c in counts.values()))
ax.set_ylim(-0.6, 1.6)
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c, _ in STYLE]
ax.legend(
    handles,
    [t for _, t, _, _ in STYLE],
    loc="lower center",
    bbox_to_anchor=(0.5, -0.04),
    ncol=3,
    frameon=False,
    fontsize=9.5,
    labelcolor=MUTED,
)
fig.suptitle(
    "An assumptions review turned many silent errors into questions",
    x=0.02,
    ha="left",
    fontsize=13,
    color=INK,
    weight="bold",
)
off_c, on_c = clear["check off"], clear["check on"]
fig.text(
    0.02,
    0.86,
    "Ambiguous tasks (21 tasks x 3 samples), Claude Haiku + Sonnet pair. "
    f"Clear twins: {off_c.get('correct', 0)} of {sum(off_c.values())} correct with the check off, "
    f"{on_c.get('correct', 0)} of {sum(on_c.values())} with it on (the rest escalated).",
    ha="left",
    fontsize=9,
    color=MUTED,
)
fig.text(
    0.02,
    -0.07,
    "One sample pair per task, same-family models, tasks shaped by earlier runs; "
    "source: results/h4, h4b, h4c.",
    ha="left",
    fontsize=8,
    color=MUTED,
)
out = ROOT / "docs" / "figures" / "assumption_check.png"
fig.savefig(out, dpi=160, facecolor=SURFACE, bbox_inches="tight")
print(out, {k: dict(v) for k, v in counts.items()}, {k: dict(v) for k, v in clear.items()})
