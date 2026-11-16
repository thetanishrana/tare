import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


dm = pd.read_parquet("/work/inputs/dm.parquet")
ex = pd.read_parquet("/work/inputs/ex.parquet")
q = ex[(ex["EXDOSE"] > 0) | ((ex["EXDOSE"] == 0) & ex["EXTRT"].str.contains("PLACEBO"))].copy()
q["d"] = pd.to_datetime(
    q["EXSTDTC"].map(lambda v: v + "-01" if len(v) == 7 else v + "-01-01" if len(v) == 4 else v),
    format="%Y-%m-%d",
    errors="coerce",
)  # partial dates imputed to the first day
q = q.dropna(subset=["d"]).sort_values(["USUBJID", "d", "EXSEQ"])
first = q.groupby("USUBJID")["d"].first()
out = dm[["USUBJID"]].copy()
out["TRTSDT"] = to_date(out["USUBJID"].map(first))
out.to_parquet("/work/out/result.parquet", index=False)
