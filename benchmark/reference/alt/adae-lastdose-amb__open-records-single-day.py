import numpy as np
import pandas as pd

ae = pd.read_parquet("/work/inputs/ae_upstream.parquet")
ex = pd.read_parquet("/work/inputs/ex.parquet")
q = ex[(ex["EXDOSE"] > 0) | ((ex["EXDOSE"] == 0) & ex["EXTRT"].str.contains("PLACEBO"))].copy()
q["s"] = pd.to_datetime(q["EXSTDTC"], format="%Y-%m-%d", errors="coerce")
q["e"] = pd.to_datetime(q["EXENDTC"], format="%Y-%m-%d", errors="coerce")
q = q[q["s"].notna()]
q["e"] = q["e"].fillna(q["s"])
by_subj = {k: g for k, g in q.groupby("USUBJID")}
ld, dose = [], []
for subj, ast in zip(ae["USUBJID"], pd.to_datetime(ae["ASTDT"])):
    g = by_subj.get(subj)
    if g is None or pd.isna(ast):
        ld.append(None)
        dose.append(np.nan)
        continue
    closed = g[g["e"].notna() & (g["s"] <= ast)]
    ld.append(max(min(e, ast) for e in closed["e"]).date() if len(closed) else None)
    cov = g[(g["s"] <= ast) & (g["e"].isna() | (g["e"] >= ast))].sort_values("s")
    dose.append(cov["EXDOSE"].iloc[-1] if len(cov) else np.nan)
out = ae[["USUBJID", "AESEQ"]].copy()
out["LDOSEDTM"] = ld
out["DOSEON"] = dose
out.to_parquet("/work/out/result.parquet", index=False)
