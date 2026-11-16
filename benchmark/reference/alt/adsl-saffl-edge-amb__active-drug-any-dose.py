import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


dm = pd.read_parquet("/work/inputs/dm.parquet")
ex = pd.read_parquet("/work/inputs/ex.parquet")
q = ex[~ex["EXTRT"].str.contains("PLACEBO")]
n = q.groupby("USUBJID").size()
out = dm[["USUBJID"]].copy()
out["SAFFL"] = out["USUBJID"].map(n).fillna(0).ge(1).map({True: "Y", False: "N"})
out.to_parquet("/work/out/result.parquet", index=False)
