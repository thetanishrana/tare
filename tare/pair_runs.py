"""Double-programming experiment runner: a config with `mode: pair` -> results/<timestamp>_<name>/.

Config keys: name, programmer_a / programmer_b ({provider, model, language, effort?}), adjudicator
({provider, model} or the string `rule`), reviewer ({provider, model} or null), prompt_version
(default k2-v4), max_repairs, samples, tasks (list or `all`), round (optional), params (sampling
parameters for the programmers; API runs send none), adjudicator_params and reviewer_params
(same, per role; reviewer_version: v1 or v2 (E8c); replay_from: a run directory whose programmers are re-parsed from its calls.jsonl instead of called again; Claude 5.5 models reject non-default sampling parameters, so leave them empty for those). Every call is logged to calls.jsonl; one record
per task sample goes to scores.jsonl, scored against the oracle only after the harness has decided.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from tare.cli_clients import make_client
from tare.harness import decide_pair, run_pair, score_harness
from tare.providers.logging_client import LoggingClient
from tare.replay import programmers_from_log
from tare.runs import RESULTS, _manifest, new_run_dir
from tare.tasks import Task, load_all_tasks


class _NoClient:
    """Stands in for the programmer client when a replay run has no model to identify."""

    model = "replay"

    def identity(self) -> dict[str, Any]:
        return {"provider": "replay", "model": "replay"}


def _client(spec: dict[str, Any] | str | None, calls_log: Path, role: str, ctx: dict[str, Any]):
    if spec is None or spec == "rule":
        return None
    return LoggingClient(make_client(spec), calls_log, role, ctx)


def run_pair_experiment(cfg: dict[str, Any], tasks: list[Task] | None = None) -> Path:
    run_dir = new_run_dir(RESULTS, cfg["name"])
    (run_dir / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))
    calls_log = run_dir / "calls.jsonl"
    ctx: dict[str, Any] = {}
    replay = Path(cfg["replay_from"]) if cfg.get("replay_from") else None
    a = None if replay else _client(cfg["programmer_a"], calls_log, "programmer_a", ctx)
    b = None if replay else _client(cfg["programmer_b"], calls_log, "programmer_b", ctx)
    adj = _client(cfg.get("adjudicator", "rule"), calls_log, "adjudicator", ctx)
    rev = _client(cfg.get("reviewer"), calls_log, "reviewer", ctx)
    manifest = _manifest(cfg, a or adj or rev or _NoClient())  # type: ignore[arg-type]
    manifest["models"] = {
        k: c.identity()
        for k, c in (("a", a), ("b", b), ("adjudicator", adj), ("reviewer", rev))
        if c
    }
    manifest.pop("model", None)
    if replay:
        manifest["replay_from"] = replay.name
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    wanted = cfg.get("tasks", "all")
    selected = [t for t in (tasks or load_all_tasks()) if wanted == "all" or t.id in wanted]
    if cfg.get("round"):
        selected = [t for t in selected if t.round == cfg["round"]]
    params = cfg.get("params") or {}
    records = []
    for task in selected:
        for s in range(cfg.get("samples", 1)):
            ctx.update(task_id=task.id, sample=s)
            lang_a = cfg["programmer_a"].get("language", "python")
            lang_b = cfg["programmer_b"].get("language", "python")
            if replay:
                pair = programmers_from_log(task, replay, s, lang_a, lang_b)
                if pair is None:
                    continue
                r = decide_pair(
                    task,
                    pair[0],
                    pair[1],
                    adj,
                    rev,
                    cfg.get("adjudicator_params"),
                    cfg.get("reviewer_params"),
                    cfg.get("reviewer_version", "v1"),
                )
            else:
                r = run_pair(
                    task,
                    a,  # type: ignore[arg-type]
                    b,  # type: ignore[arg-type]
                    adj,
                    rev,
                    lang_a,
                    lang_b,
                    cfg.get("prompt_version", "k2-v4"),
                    cfg.get("max_repairs", 2),
                    params,
                    cfg.get("adjudicator_params"),
                    cfg.get("reviewer_params"),
                    cfg.get("reviewer_version", "v1"),
                )
            sc = score_harness(task, r).to_dict()
            rec = {
                "task_id": task.id,
                "sample": s,
                "ambiguous": task.ambiguous,
                "round": task.round,
                "decision": r.decision,
                "source": r.source,
                "class": sc["class"],
                "reason": r.reason,
                "question": r.question,
                "a_status": r.a.status,
                "b_status": r.b.status,
                "a_assumptions": r.a.assumptions,
                "b_assumptions": r.b.assumptions,
                "programmers_agree": r.compare.agree if r.compare else None,
                "diff_records": r.compare.mismatched_records if r.compare else None,
                "output_digest": sc.get("output_digest"),
                "matches_reading": sc.get("matches_reading"),
                "mismatched_records": sc.get("mismatched_records"),
                "tokens": r.a.input_tokens
                + r.a.output_tokens
                + r.b.input_tokens
                + r.b.output_tokens,
            }
            records.append(rec)
            print(
                f"{task.id:26s} s{s} {rec['class']:13s} decision={r.decision} source={r.source} "
                f"a={r.a.status} b={r.b.status}",
                flush=True,
            )
            with (run_dir / "scores.jsonl").open("a") as f:
                f.write(json.dumps(rec) + "\n")
    summary = {
        "n_samples": len(records),
        "classes": dict(Counter(r["class"] for r in records)),
        "decisions": dict(Counter(r["decision"] for r in records)),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    print("summary:", summary)
    return run_dir
