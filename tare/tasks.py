"""Task definitions and bundle building.

A task YAML (benchmark/tasks/<id>.yaml) names the inputs a programmer may read, the output contract
and the oracle that holds the answer. `build_bundle` writes what a programmer sees:

    data/tasks/<id>/inputs/*.parquet, spec.md, contract.json, data_description.md

and `build_answer` writes the hidden answer key to data/answers/<id>.parquet, a separate tree that
is never mounted into a sandbox or shown in a prompt.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import yaml

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "benchmark" / "tasks"
BENCHMARK = ROOT / "benchmark"
SDTM_DIR = ROOT / "data" / "sdtm"
ORACLE_DIR = ROOT / "data" / "oracle"
BUNDLES_DIR = ROOT / "data" / "tasks"
ANSWERS_DIR = ROOT / "data" / "answers"


@dataclass
class Task:
    raw: dict[str, Any]

    @property
    def id(self) -> str:
        return self.raw["id"]

    @property
    def keys(self) -> list[str]:
        return list(self.raw["keys"])

    @property
    def target_vars(self) -> list[str]:
        return list(self.raw["target_vars"])

    @property
    def columns(self) -> dict[str, str]:
        return dict(self.raw["output_contract"]["columns"])

    @property
    def oracle_id(self) -> str:
        return self.raw["oracle_id"]

    @property
    def dataset(self) -> str:
        return self.raw["dataset"].lower()

    @property
    def rows(self) -> dict[str, Any]:
        return self.raw.get("rows") or {}

    @property
    def round(self) -> str:
        return self.raw.get("round", "k2a")

    @property
    def ambiguous(self) -> bool:
        return bool(self.raw.get("ambiguous", False))

    @property
    def readings(self) -> list[dict[str, str]]:
        """Alternative defensible readings of an ambiguous spec: [{id, description}]."""
        return list(self.raw.get("readings") or [])

    @property
    def split(self) -> str:
        return self.raw["split"]

    def contract(self) -> dict[str, Any]:
        c = self.raw["output_contract"]
        return {
            "columns": c["columns"],
            "keys": self.keys,
            "target_vars": self.target_vars,
            "allowed_values": c.get("allowed_values") or {},
            "nullable": c.get("nullable") or [],
        }


def alt_answer_path(task_id: str, reading_id: str) -> Path:
    return ANSWERS_DIR / f"{task_id}__{reading_id}.parquet"


def load_task(task_id: str) -> Task:
    return Task(yaml.safe_load((TASKS_DIR / f"{task_id}.yaml").read_text()))


def load_all_tasks() -> list[Task]:
    return [Task(yaml.safe_load(p.read_text())) for p in sorted(TASKS_DIR.glob("*.yaml"))]


def _apply_rows(df: pd.DataFrame, rows: dict[str, Any]) -> pd.DataFrame:
    for col, val in rows.items():
        if val is None:
            df = df[df[col].isna()]
        elif isinstance(val, dict) and "not" in val:
            df = df[~df[col].isin(val["not"])]
        elif isinstance(val, list):
            df = df[df[col].isin(val)]
        else:
            df = df[df[col] == val]
    return df


def _fill_missing(df: pd.DataFrame, fill: dict[str, Any]) -> pd.DataFrame:
    """Replace nulls in the named columns, so a column can serve as a key (task field `fill_missing`)."""
    for col, val in fill.items():
        if col in df.columns:
            df = df.assign(**{col: df[col].fillna(val)})
    return df


def _read_input(task: Task, spec: dict[str, Any]) -> pd.DataFrame:
    if spec["source"] == "sdtm":
        # an sdtm input may name an oracle whose perturbed copy of that domain replaces the original
        if spec.get("oracle_id"):
            df = pd.read_parquet(
                ORACLE_DIR / spec["oracle_id"] / "sdtm" / f"{spec['name']}.parquet"
            )
        else:
            df = pd.read_parquet(SDTM_DIR / f"{spec['name']}.parquet")
    elif spec["source"] == "oracle":
        df = pd.read_parquet(ORACLE_DIR / spec["oracle_id"] / f"{spec['dataset']}.parquet")
        df = _apply_rows(df, task.rows)
        df = _fill_missing(df, task.raw.get("fill_missing") or {})
    else:
        raise ValueError(f"unknown input source {spec['source']!r}")
    cols = spec.get("columns", "all")
    if cols != "all":
        df = df[list(cols)]
    return df.reset_index(drop=True)


def build_answer(task: Task) -> pd.DataFrame:
    df = pd.read_parquet(ORACLE_DIR / task.oracle_id / f"{task.dataset}.parquet")
    df = _apply_rows(df, task.raw.get("answer_rows", task.rows))
    df = _fill_missing(df, task.raw.get("fill_missing") or {})
    ans = df[task.keys + task.target_vars].reset_index(drop=True)
    if ans.duplicated(task.keys).any():
        raise ValueError(f"{task.id}: answer keys {task.keys} are not unique")
    return ans


def _describe_column(s: pd.Series) -> str:
    n = len(s)
    missing = s.isna().sum()
    if s.dtype == object or str(s.dtype) in ("str", "string"):
        empty = int((s == "").sum())
        miss_txt = f"{missing / n:.0%} null" if missing else "no nulls"
        if empty:
            miss_txt += f", {empty / n:.0%} empty strings"
        nun = s.nunique()
        sample = s.dropna().unique()[:6]
        if s.dropna().map(lambda v: hasattr(v, "year")).all() and len(s.dropna()):
            return f"date; {miss_txt}; range {s.dropna().min()} to {s.dropna().max()}"
        levels = (
            f"levels: {sorted(map(str, s.dropna().unique()))}"
            if nun <= 12
            else f"{nun} distinct, e.g. {list(map(str, sample))}"
        )
        return f"string; {miss_txt}; {levels}"
    if str(s.dtype).startswith("datetime"):
        return f"datetime; {missing / n:.0%} null"
    nn = s.dropna()
    rng = f"range {nn.min():g} to {nn.max():g}" if len(nn) else "all null"
    kind = "integer-valued number" if len(nn) and (nn == nn.round()).all() else "number"
    return f"{kind}; {missing / n:.0%} null; {rng}"


def data_description(inputs: dict[str, pd.DataFrame], sources: dict[str, str]) -> str:
    out = ["# Input data", ""]
    out.append(
        "Files are in `inputs/` as parquet. Missing values in SDTM inputs (source: sdtm) are mostly empty "
        "strings for character columns and null for numbers; inputs from an upstream ADaM dataset "
        "(source: upstream) use null for every missing value."
    )
    for name, df in inputs.items():
        out += [
            "",
            f"## `{name}.parquet` ({sources[name]}): {len(df)} rows, {df.shape[1]} columns",
            "",
        ]
        out += ["| column | description |", "|---|---|"]
        for c in df.columns:
            out.append(f"| {c} | {_describe_column(df[c])} |")
    return "\n".join(out) + "\n"


def build_bundle(task: Task) -> Path:
    bundle = BUNDLES_DIR / task.id
    if bundle.exists():
        shutil.rmtree(bundle)
    (bundle / "inputs").mkdir(parents=True)
    frames, sources = {}, {}
    for spec in task.raw["inputs"]:
        df = _read_input(task, spec)
        frames[spec["name"]] = df
        sources[spec["name"]] = "sdtm" if spec["source"] == "sdtm" else "upstream"
        df.to_parquet(bundle / "inputs" / f"{spec['name']}.parquet", index=False)
    shutil.copy(BENCHMARK / task.raw["spec"], bundle / "spec.md")
    (bundle / "contract.json").write_text(json.dumps(task.contract(), indent=2) + "\n")
    (bundle / "data_description.md").write_text(data_description(frames, sources))
    ANSWERS_DIR.mkdir(parents=True, exist_ok=True)
    build_answer(task).to_parquet(ANSWERS_DIR / f"{task.id}.parquet", index=False)
    return bundle


def build_all() -> list[Path]:
    return [build_bundle(t) for t in load_all_tasks()]


def arrow_type_name(t: pa.DataType) -> str:
    if pa.types.is_string(t) or pa.types.is_large_string(t):
        return "string"
    if pa.types.is_date(t) or pa.types.is_timestamp(t):
        return "date"
    if pa.types.is_integer(t) or pa.types.is_floating(t):
        return "number"
    return str(t)


def read_schema(path: Path) -> dict[str, str]:
    schema = pq.read_schema(path)
    return {f.name: arrow_type_name(f.type) for f in schema}
