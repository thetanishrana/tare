"""Single-programmer experiment runner (E0 style): prompt -> code -> sandbox -> score, with repairs.

Every run writes to its own directory under results/ with a copy of its config, the git commit,
package versions, every model call (calls.jsonl) and one score record per task sample (scores.jsonl).
Repairs only fix loud errors; the model never sees the answer key, only its own stderr and the
structural contract problems.
"""

from __future__ import annotations

import datetime as dt
import importlib.metadata as md
import json
import platform
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from tare.pricing import cost_usd
from tare.prompts import (
    ESCALATION_VERSIONS,
    PROMPT_VERSION,
    build_messages,
    build_repair_messages,
    extract_assumptions,
    extract_code,
    extract_escalation,
    task_files_hash,
)
from tare.providers.base import ModelClient
from tare.run_task import run_and_score
from tare.sandbox.runner import SandboxResult
from tare.score import LOUD

ESCALATED = "escalated"
from tare.tasks import BENCHMARK, ROOT, Task, load_all_tasks

RESULTS = ROOT / "results"


def new_run_dir(base: Path, name: str) -> Path:
    """Create `<timestamp>_<name>` under base; a repeat within the same second gets a `-2`, `-3` suffix."""
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base / f"{stamp}_{name}"
    n = 1
    while True:
        try:
            run_dir.mkdir(parents=True)
            return run_dir
        except FileExistsError:
            n += 1
            run_dir = base / f"{stamp}-{n}_{name}"


PACKAGES = ["pandas", "pyarrow", "numpy", "openai", "anthropic", "pyyaml", "pydantic"]


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()
        return out + ("+dirty" if dirty else "")
    except OSError:
        return "unknown"


def _manifest(cfg: dict[str, Any], client: ModelClient) -> dict[str, Any]:
    versions = {}
    for p in PACKAGES:
        try:
            versions[p] = md.version(p)
        except md.PackageNotFoundError:
            pass
    return {
        "git_commit": _git_commit(),
        "benchmark_version": (BENCHMARK / "BENCHMARK_VERSION").read_text().strip(),
        "task_files_sha256": task_files_hash(BENCHMARK / "tasks")
        + "/"
        + task_files_hash(BENCHMARK / "specs"),
        "prompt_version": cfg.get("prompt_version", PROMPT_VERSION),
        "model": client.identity(),
        "python": platform.python_version(),
        "python_packages": versions,
        "sandbox_image": "tare-sandbox:dev",
        "started": dt.datetime.now(dt.UTC).isoformat(),
    }


def _feedback(res: SandboxResult | None, problems: list[str], no_code: bool) -> str:
    if no_code:
        return "Your reply did not contain a fenced code block."
    parts = []
    if res is not None and not res.ok:
        status = "timed out" if res.timed_out else f"exit code {res.exit_code}"
        parts.append(f"The script failed ({status}).\nstderr (end):\n{res.stderr[-2500:]}")
    if problems:
        parts.append("Problems with the output file:\n- " + "\n- ".join(problems))
    return "\n\n".join(parts) or "The script produced no output file at /work/out/result.parquet."


def run_sample(
    task: Task,
    client: ModelClient,
    cfg: dict[str, Any],
    calls_log: Path,
    run_dir: Path,
    sample: int,
) -> dict[str, Any]:
    language = cfg["language"]
    params = {"max_tokens": cfg.get("max_tokens", 4096)}
    if "temperature" in cfg:  # API runs omit it (Claude 5.5 models reject non-default sampling)
        params["temperature"] = cfg["temperature"]
    messages = build_messages(task, language, cfg.get("prompt_version", PROMPT_VERSION))
    sample_dir = run_dir / task.id / f"s{sample}"
    sample_dir.mkdir(parents=True, exist_ok=True)
    rec: dict[str, Any] = {
        "task_id": task.id,
        "sample": sample,
        "attempts": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "latency_s": 0.0,
    }
    code, score, res = None, None, None
    for attempt in range(cfg.get("max_repairs", 2) + 1):
        comp = client.complete(messages, **params)
        rec["attempts"] += 1
        rec["input_tokens"] += comp.usage.input_tokens
        rec["output_tokens"] += comp.usage.output_tokens
        rec["latency_s"] += comp.latency_s
        with calls_log.open("a") as f:
            f.write(
                json.dumps(
                    {
                        "task_id": task.id,
                        "sample": sample,
                        "attempt": attempt,
                        "model": comp.model,
                        "params": comp.params or params,
                        "messages": messages,
                        "response": comp.text,
                        "usage": vars(comp.usage),
                        "stop_reason": comp.stop_reason,
                        "latency_s": comp.latency_s,
                    }
                )
                + "\n"
            )
        question = (
            extract_escalation(comp.text)
            if cfg.get("prompt_version") in ESCALATION_VERSIONS
            else None
        )
        if question is not None:
            (sample_dir / f"response_{attempt}.md").write_text(comp.text)
            rec.update(
                {
                    "class": ESCALATED,
                    "problems": [],
                    "question": question,
                    "mismatched_records": None,
                    "ambiguous": task.ambiguous,
                    "round": task.round,
                    "assumptions": extract_assumptions(comp.text),
                }
            )
            rec["cost_usd"] = cost_usd(client.model, rec["input_tokens"], rec["output_tokens"])
            (sample_dir / "score.json").write_text(json.dumps(rec, indent=2))
            return rec
        code = extract_code(comp.text, language)
        found = extract_assumptions(comp.text)
        if found:
            rec["assumptions"] = found
        (sample_dir / f"response_{attempt}.md").write_text(comp.text)
        if code is None:
            score, res, no_code = None, None, True
            problems = ["no code block in the reply"]
        else:
            no_code = False
            (sample_dir / f"code_{attempt}.{'py' if language == 'python' else 'R'}").write_text(
                code
            )
            score, res = run_and_score(task, code, language, timeout=cfg.get("timeout", 120))
            problems = score.problems
        if score is not None and score.klass != LOUD:
            break
        if attempt < cfg.get("max_repairs", 2):
            messages = build_repair_messages(
                messages, code or "", language, _feedback(res, problems, no_code)
            )
    if score is None:
        rec.update(
            {"class": LOUD, "problems": ["no code block in the reply"], "mismatched_records": None}
        )
    else:
        d = score.to_dict()
        d.pop("sample", None)  # record-level answer values stay out of the logs we share
        rec.update(
            {
                k: d.get(k)
                for k in (
                    "class",
                    "problems",
                    "output_digest",
                    "matches_reading",
                    "mismatches",
                    "mismatched_records",
                    "mismatch_share",
                    "n_answer",
                    "n_output",
                )
            }
        )
        if res is not None:
            rec["stderr_tail"] = None if res.ok else res.stderr[-500:]
    rec["ambiguous"], rec["round"] = task.ambiguous, task.round
    rec["cost_usd"] = cost_usd(client.model, rec["input_tokens"], rec["output_tokens"])
    (sample_dir / "score.json").write_text(json.dumps(rec, indent=2))
    return rec


def run_experiment(
    cfg: dict[str, Any],
    client: ModelClient,
    run_name: str | None = None,
    tasks: list[Task] | None = None,
) -> Path:
    run_dir = new_run_dir(RESULTS, run_name or cfg["name"])
    (run_dir / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))
    (run_dir / "manifest.json").write_text(json.dumps(_manifest(cfg, client), indent=2))
    calls_log = run_dir / "calls.jsonl"
    all_tasks = tasks if tasks is not None else load_all_tasks()
    wanted = cfg.get("tasks", "all")
    selected = [t for t in all_tasks if wanted == "all" or t.id in wanted]
    if cfg.get("round"):
        selected = [t for t in selected if t.round == cfg["round"]]
    records = []
    for task in selected:
        for s in range(cfg.get("samples", 1)):
            rec = run_sample(task, client, cfg, calls_log, run_dir, s)
            records.append(rec)
            print(
                f"{task.id:24s} s{s} {rec['class']:13s} attempts={rec['attempts']} mismatched={rec.get('mismatched_records')}",
                flush=True,
            )
            with (run_dir / "scores.jsonl").open("a") as f:
                f.write(json.dumps(rec) + "\n")
    counts = Counter(r["class"] for r in records)
    costs = [r["cost_usd"] for r in records if r.get("cost_usd") is not None]
    summary = {
        "n_samples": len(records),
        "classes": dict(counts),
        "cost_usd_total": round(sum(costs), 4) if costs else None,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print("summary:", summary)
    return run_dir
