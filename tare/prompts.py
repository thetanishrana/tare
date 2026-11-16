"""Prompt template (versioned) and code extraction for the single-programmer runs."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tare.tasks import BUNDLES_DIR, Task

PROMPT_VERSION = "k2-v1"
PROMPT_VERSIONS = ("k2-v1", "k2-v2", "k2-v3", "k2-v4")
# v1: no escalation option; v2: optional ESCALATE reply; v3: stronger instruction (E8);
# v4: v3 plus a required ASSUMPTIONS list and a checklist of common ambiguities (E8).
ESCALATION_VERSIONS = ("k2-v2", "k2-v3", "k2-v4")

LANG = {
    "python": ("Python 3 (pandas, numpy and pyarrow are installed)", "python", "code.py"),
    "r": ("R (dplyr, lubridate, stringr, admiral and arrow are installed)", "r", "code.R"),
}

ESCALATE_TEXT = """
# If the spec is not clear enough

If the spec leaves open a point that would change the output, and a competent clinical programmer would ask the study team before coding rather than choose, do not guess. Reply with exactly one line `ESCALATE: <your single most important question>` and no code. Escalate only when a real question remains; if the spec is clear enough to implement, write the script.
"""

ESCALATE_TEXT_V3 = """
# Check the spec before you code

Spec ambiguity is a common cause of wrong clinical datasets, and silently guessing is the failure we most want to avoid. Before writing any code, read the spec once more and ask: is there a point where two reasonable readings would give a different output? If so, and the spec does not settle it, do not choose one yourself: reply with exactly one line `ESCALATE: <your single most important question>` and no code. If every point that could change the output is settled by the spec, write the script. Do not ask about things the spec already answers.
"""

ESCALATE_TEXT_V4 = """
# Check the spec before you code

Spec ambiguity is a common cause of wrong clinical datasets, and silently guessing is the failure we most want to avoid. Go through this checklist against the spec:

- Is a date boundary inclusive or exclusive (on or before versus before, on or after versus after)?
- Which datasets, records or sources count, and which are left out (for example placebo or zero-dose rows, missing values, extra domains)?
- How are ties and ordering decided?
- How are partial or missing dates and missing values handled?
- Is a count or duration inclusive or exclusive of the end points?
- Is a date compared as a date, or as a date with a time?

Start your reply with a line `ASSUMPTIONS:` followed by a short list of every choice you had to make where the spec could be read more than one way (write `none` if there is no such choice). Then:

- if any listed choice would change the output and the spec does not settle it, ask: add exactly one line `ESCALATE: <your single most important question>` and give no code;
- otherwise give the script as one fenced code block.
"""

SYSTEM = (
    "You are an experienced clinical statistical programmer. You write correct, plain, deterministic code "
    "that derives CDISC ADaM variables exactly as a derivation spec says. Follow the spec literally, "
    "including edge cases."
)


def _contract_text(task: Task) -> str:
    c = task.contract()
    lines = ["Output columns (exactly these, in any order; extra columns are ignored):"]
    for col, kind in c["columns"].items():
        extra = []
        if col in c["keys"]:
            extra.append("key")
        if col in c["nullable"]:
            extra.append("may be null")
        if col in c["allowed_values"]:
            extra.append("allowed values: " + ", ".join(map(str, c["allowed_values"][col])))
        lines.append(f"- `{col}`: {kind}" + (f" ({'; '.join(extra)})" if extra else ""))
    lines.append("")
    lines.append(
        "Type rules: `string` columns hold text or null; `date` columns must be written as calendar dates "
        "(date32, or a timestamp at midnight); `number` columns are numeric. Write missing values as real nulls, "
        "never as empty strings or the text 'NA'. Keys must be unique and must cover exactly the rows the spec asks for."
    )
    return "\n".join(lines)


ESCALATION_TEXT = {"k2-v2": ESCALATE_TEXT, "k2-v3": ESCALATE_TEXT_V3, "k2-v4": ESCALATE_TEXT_V4}


def build_messages(
    task: Task, language: str, version: str = PROMPT_VERSION
) -> list[dict[str, str]]:
    bundle = BUNDLES_DIR / task.id
    spec = (bundle / "spec.md").read_text()
    desc = (bundle / "data_description.md").read_text()
    label, fence, _ = LANG[language]
    user = f"""Derive the target variable(s) for this task with a complete {label} script.

# Task spec

{spec}

{desc}

# Output

{_contract_text(task)}

# How your script runs

- It runs with no network access. Input parquet files are in `/work/inputs/`; write the result to `/work/out/result.parquet`.
- Reply with exactly one fenced ```{fence} code block containing the whole script, and nothing else you need me to run.
{ESCALATION_TEXT.get(version, "")}"""
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]


def build_repair_messages(
    messages: list[dict[str, str]], code: str, language: str, feedback: str
) -> list[dict[str, str]]:
    fence = LANG[language][1]
    return [
        *messages,
        {"role": "assistant", "content": f"```{fence}\n{code}\n```"},
        {
            "role": "user",
            "content": f"Running your script failed:\n\n{feedback}\n\nFix the script. Reply with exactly one fenced ```{fence} code block containing the complete corrected script.",
        },
    ]


_ASSUMPTIONS = re.compile(
    r"^\s*ASSUMPTIONS:\s*(.*?)(?=^\s*(?:ESCALATE:|```)|\Z)", re.MULTILINE | re.DOTALL
)


def extract_assumptions(text: str) -> str | None:
    """The text of the ASSUMPTIONS: section (prompt k2-v4), if the reply has one."""
    m = _ASSUMPTIONS.search(text)
    return m.group(1).strip() if m else None


_ESCALATE = re.compile(r"^\s*ESCALATE:\s*(.+?)\s*$", re.MULTILINE)


def extract_escalation(text: str) -> str | None:
    """The question if the reply is an escalation (an ESCALATE: line and no code block), else None."""
    if _FENCE.search(text):
        return None
    m = _ESCALATE.search(text)
    return m.group(1) if m else None


_FENCE = re.compile(r"```[ \t]*([A-Za-z0-9_+-]*)[ \t]*\n(.*?)```", re.DOTALL)


def extract_code(text: str, language: str) -> str | None:
    """The last fenced block tagged with the language (or untagged); None if there is none."""
    wanted = {"python": {"python", "py", "python3"}, "r": {"r"}}[language]
    blocks = [(tag.lower(), body) for tag, body in _FENCE.findall(text)]
    matching = [b for tag, b in blocks if tag in wanted or tag == ""]
    return matching[-1].rstrip() + "\n" if matching else None


def task_files_hash(tasks_dir: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    for p in sorted(tasks_dir.rglob("*")):
        if p.is_file():
            h.update(p.name.encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def contract_json(task: Task) -> str:
    return json.dumps(task.contract(), indent=2)


# E8b: a separate reviewer sees only the spec and the programmer's assumptions list.
REVIEWER_PROMPT = """You are reviewing a spec for a clinical trial dataset derivation before any code is accepted. A programmer read the spec and listed the assumptions they made. You see only the spec and that list.

Decide whether any listed assumption is a choice the spec does not settle, where a different reasonable choice would change the values in the output. If so, the programmer should have asked the study team instead of choosing.

- If there is such a choice, reply with exactly one line `ESCALATE: <your question, naming the specific choice and the competing options>` and nothing else.
- If every listed assumption is stated by the spec, or is a harmless default that cannot change the output, reply with exactly `PROCEED`.

Do not escalate on choices the spec already states. Do not escalate on points that merely restate the spec in other words.

# Spec

{spec}

# Programmer's assumptions

{assumptions}
"""


def build_review_messages(spec: str, assumptions: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": REVIEWER_PROMPT.format(spec=spec.strip(), assumptions=assumptions.strip()),
        }
    ]


# E8c: reviewer that must write out the competing readings (docs/09_DECISIONS.md, 2026-11-04). Fixed
# before any run; the escalation rule is applied in code (tare/review.py), not by the model.
REVIEWER_PROMPT_V2 = """You are reviewing a spec for a clinical trial dataset derivation before any code is accepted. Two programmers independently read the spec and each listed the assumptions they made. You see only the spec and those lists.

Step 1. List every distinct choice made in either list (merge choices that are the same).
Step 2. For each choice, write the competing readings a careful programmer could take from the spec text alone.
Step 3. Say whether the spec's own words settle the choice (`spec_settles`), quoting the words if they do. Two programmers agreeing on a reading does not settle it, and neither does a reading being common practice.
Step 4. Say whether choosing a different reading would change which records get which values in the output (`changes_output`: "yes", "no" or "unknown").

Reply with one JSON object and nothing else:
{{"choices": [{{"choice": "<the choice>", "readings": ["<reading 1>", "<reading 2>"], "spec_settles": true or false, "quote": "<spec words or empty>", "changes_output": "yes" | "no" | "unknown", "question": "<one precise question for the study team, naming the readings>"}}]}}

# Spec

{spec}

# Programmers' assumptions

{assumptions}
"""


def build_review_messages_v2(spec: str, assumptions: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": REVIEWER_PROMPT_V2.format(
                spec=spec.strip(), assumptions=assumptions.strip()
            ),
        }
    ]
