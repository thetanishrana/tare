import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


import datetime as dt

dm = pd.read_parquet("/work/inputs/dm.parquet")
ae = pd.read_parquet("/work/inputs/ae.parquet")
lb = pd.read_parquet("/work/inputs/lb.parquet")
vs = pd.read_parquet("/work/inputs/vs.parquet")
up = pd.read_parquet("/work/inputs/adsl_upstream.parquet")


def first_of_period(dtc):
    """Date part of an ISO 8601 string; a missing month or day is filled with 1."""
    if dtc is None or pd.isna(dtc) or dtc == "":
        return None
    p = dtc[:10].split("-")
    return dt.date(int(p[0]), int(p[1]) if len(p) > 1 else 1, int(p[2]) if len(p) > 2 else 1)


cands = []
for df, col in [(ae, "AESTDTC"), (ae, "AEENDTC"), (lb, "LBDTC"), (vs, "VSDTC")]:
    for subj, dtc in zip(df["USUBJID"], df[col]):
        d = first_of_period(dtc)
        if d:
            cands.append((subj, d))
for subj, d in zip(up["USUBJID"], up["TRTEDT"]):
    if pd.notna(d):
        cands.append((subj, d))
best = {}
for subj, d in cands:
    if subj not in best or d > best[subj]:
        best[subj] = d
out = dm[["USUBJID"]].copy()
out["LSTALVDT"] = out["USUBJID"].map(best)
out.to_parquet("/work/out/result.parquet", index=False)
