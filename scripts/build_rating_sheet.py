"""Build a blinded ambiguity-rating sheet from the *-amb specs and their clear twins.

Writes docs/ratings/rating_sheet.md (no labels, shuffled) and
docs/ratings/rating_key.md (which item is which). Rater must not see the key.
`python scripts/build_rating_sheet.py u1` writes the same for the unseen set u1 into
rating_sheet_u1.md and rating_key_u1.md and leaves the v1.0 sheet alone.
"""

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "benchmark" / "specs"
OUT = ROOT / "docs" / "ratings"
PAIRS = [
    "adae-trtemfl",
    "adlb-ablfl",
    "adsl-lstalvdt",
    "adsl-saffl",
    "adsl-trtdurd",
    "adsl-trtsdt",
    "adsl-eosstt",
    "adae-astdt",
    "adae-aoccifl",
    "adlb-chg",
    "adlb-ontrtfl",
    "advs-average",
    "advs-ablfl",
    "adae-lastdose",
    "adae-aendt-pdates",
    "adoe-iop-ablfl",
    "adae-aestudyeye",
    "adsl-dispdates",
    "advs-chg",
    "adlb-shift1",
    "adae-astdy",
    "adae-adurn",
    "adlb-pchg",
    "adlb-anrind",
]

PAIRS_U1 = [
    "advs-ontrtfl",
    "advs-anl01fl",
    "adsl-trtedt-edge",
    "adlb-r2base",
    "advs-avisit",
    "advs-ady",
    "advs-ontrtfl-edge",
    "advs-ablfl-edge",
    "adae-trtemfl-pdates",
    "adae-astdy-pdates",
    "advs-chg-edge",
    "adae-aoccifl-aedates",
    "adlb-ablfl-edge",
    "adae-lastdose-edge",
]
SET = sys.argv[1] if len(sys.argv) > 1 else ""
SUFFIX = "_u1" if SET == "u1" else ""
items = []
for p in PAIRS_U1 if SET == "u1" else PAIRS:
    items.append((f"{p}-amb", True))
    items.append((f"{p}-std", False))
random.Random(20261027).shuffle(items)

sheet = [
    "# Spec ambiguity rating sheet",
    "",
    "Each item below is a short specification for deriving one ADaM variable from SDTM-derived inputs. For each, imagine you are the programmer and answer:",
    "",
    "1. **Ambiguous?** Would you need to ask a question before programming it? (yes / no)",
    "2. **Open point:** if yes, what exactly is unclear? (one sentence)",
    "3. **Confidence:** low / medium / high",
    "",
    "Please rate from the text alone. Specs are fictional task text, not a real study.",
    "",
]
key = [
    "# Rating key (do not show raters)",
    "",
    "| Item | Task id | Author label |",
    "|---|---|---|",
]
for i, (tid, amb) in enumerate(items, 1):
    text = (SPECS / f"{tid}.md").read_text().strip()
    sheet += [
        f"## Item {i}",
        "",
        text,
        "",
        "- Ambiguous? (yes/no): ",
        "- Open point: ",
        "- Confidence: ",
        "",
    ]
    key.append(f"| {i} | {tid} | {'ambiguous' if amb else 'clear'} |")

OUT.mkdir(parents=True, exist_ok=True)
(OUT / f"rating_sheet{SUFFIX}.md").write_text("\n".join(sheet) + "\n")
(OUT / f"rating_key{SUFFIX}.md").write_text("\n".join(key) + "\n")
