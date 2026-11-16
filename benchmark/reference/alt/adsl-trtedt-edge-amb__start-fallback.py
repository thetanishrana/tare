import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


dm = pd.read_parquet("/work/inputs/dm.parquet")
ex = pd.read_parquet("/work/inputs/ex.parquet")
q = ex[(ex["EXDOSE"] > 0) | ((ex["EXDOSE"] == 0) & ex["EXTRT"].str.contains("PLACEBO"))].copy()
q["d"] = pd.to_datetime(q["EXENDTC"], format="%Y-%m-%d", errors="coerce")  # complete dates only
q["d"] = q["d"].fillna(pd.to_datetime(q["EXSTDTC"], format="%Y-%m-%d", errors="coerce"))
last = q.dropna(subset=["d"]).groupby("USUBJID")["d"].max()
out = dm[["USUBJID"]].copy()
out["TRTEDT"] = to_date(out["USUBJID"].map(last))
out.to_parquet("/work/out/result.parquet", index=False)
