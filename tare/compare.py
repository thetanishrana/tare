"""Deterministic comparison of an output dataset against an answer (or another output).

The scorer and the double-programming comparator use this same code, so "agreement" and
"correctness" are measured identically.

Normalization (documented choices):
  * string columns: empty string is treated as missing (null);
  * date columns: date, date64 and timestamp are all accepted and truncated to a calendar date;
  * numbers: equal if |a - b| <= 1e-8 * max(1, |a|); null equals null, null versus a value mismatches;
  * extra columns beyond the contract are ignored.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tare.tasks import read_schema

TOL = 1e-8


@dataclass
class CompareResult:
    agree: bool
    n_left: int
    n_right: int
    missing_keys: int = 0  # keys in left (answer) absent from right (output)
    extra_keys: int = 0
    mismatches: dict[str, int] = field(default_factory=dict)  # target var -> mismatching records
    mismatched_records: int = 0  # records with at least one mismatching target
    sample: list[dict[str, Any]] = field(default_factory=list)


def _norm_column(s: pd.Series, kind: str) -> pd.Series:
    if kind == "string":
        s = s.astype(object).where(s.notna(), None)
        return s.map(lambda v: None if v is None or v == "" else str(v))
    if kind == "date":
        d = pd.to_datetime(s, errors="coerce")
        if (
            getattr(d.dt, "tz", None) is not None
        ):  # tz-aware timestamps (e.g. R POSIXct in UTC) -> naive
            d = d.dt.tz_localize(None)
        return d.dt.normalize()
    return pd.to_numeric(s, errors="coerce").astype(float)


def _equal(a: pd.Series, b: pd.Series, kind: str) -> pd.Series:
    if kind == "number":
        both_na = a.isna() & b.isna()
        close = (a - b).abs() <= TOL * np.maximum(1.0, a.abs())
        return both_na | (close.fillna(False))
    if kind == "date":
        return (a.isna() & b.isna()) | (a == b)
    an, bn = a.isna(), b.isna()
    return (an & bn) | (~an & ~bn & (a == b))


def compare_frames(
    left: pd.DataFrame,
    right: pd.DataFrame,
    keys: list[str],
    targets: list[str],
    kinds: dict[str, str],
    sample_size: int = 10,
) -> CompareResult:
    """Compare `right` (output) against `left` (answer) on `targets`, joined on `keys`."""
    lft = left[keys + targets].copy()
    rgt = right[keys + targets].copy()
    for k in keys:
        if kinds[k] == "number":
            lft[k] = pd.to_numeric(lft[k]).astype(float)
            rgt[k] = pd.to_numeric(rgt[k]).astype(float)
        else:
            lft[k] = lft[k].astype(str)
            rgt[k] = rgt[k].astype(str)
    m = lft.merge(rgt, on=keys, how="outer", suffixes=("__a", "__b"), indicator=True)
    both = m[m["_merge"] == "both"]
    res = CompareResult(
        agree=False,
        n_left=len(lft),
        n_right=len(rgt),
        missing_keys=int((m["_merge"] == "left_only").sum()),
        extra_keys=int((m["_merge"] == "right_only").sum()),
    )
    bad_any = pd.Series(False, index=both.index)
    for t in targets:
        a = _norm_column(both[t + "__a"], kinds[t])
        b = _norm_column(both[t + "__b"], kinds[t])
        ok = _equal(a, b, kinds[t])
        res.mismatches[t] = int((~ok).sum())
        bad_any |= ~ok
    res.mismatched_records = int(bad_any.sum())
    for _, row in both[bad_any].head(sample_size).iterrows():
        res.sample.append(
            {c: (None if pd.isna(row[c]) else str(row[c])) for c in both.columns if c != "_merge"}
        )
    res.agree = res.missing_keys == 0 and res.extra_keys == 0 and res.mismatched_records == 0
    return res


def contract_violations(output_path: Path, contract: dict[str, Any], df: pd.DataFrame) -> list[str]:
    """Structural checks: columns, types, nulls, allowed values, key uniqueness."""
    problems: list[str] = []
    schema = read_schema(output_path)
    for col, kind in contract["columns"].items():
        if col not in schema:
            problems.append(f"missing column {col}")
        elif schema[col] != kind:
            problems.append(f"column {col} has type {schema[col]}, expected {kind}")
    if problems:
        return problems
    nullable = set(contract.get("nullable") or [])
    for col in contract["columns"]:
        if col not in nullable and df[col].isna().any():
            problems.append(f"column {col} has nulls but is not nullable")
    for col, allowed in (contract.get("allowed_values") or {}).items():
        vals = _norm_column(df[col], "string").dropna().unique()
        bad = [v for v in vals if v not in set(map(str, allowed))]
        if bad:
            problems.append(f"column {col} has values outside the allowed set: {bad[:5]}")
    if df.duplicated(contract["keys"]).any():
        problems.append(f"duplicate keys {contract['keys']}")
    return problems


def output_digest(
    df: pd.DataFrame, keys: list[str], targets: list[str], kinds: dict[str, str]
) -> str:
    """Stable fingerprint of the normalized key and target values, for same-wrong-output counting."""
    cols = keys + targets
    norm = pd.DataFrame({c: _norm_column(df[c], kinds[c]) for c in cols})
    for c in cols:
        if kinds[c] == "number":
            norm[c] = norm[c].round(8)
    norm = norm.sort_values(keys, kind="stable").reset_index(drop=True)
    return hashlib.sha256(norm.to_csv(index=False, na_rep="<NA>").encode()).hexdigest()[:16]
