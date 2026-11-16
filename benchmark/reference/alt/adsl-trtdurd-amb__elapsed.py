import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


u = pd.read_parquet("/work/inputs/adsl_upstream.parquet")
s = pd.to_datetime(u["TRTSDT"])
e = pd.to_datetime(u["TRTEDT"])
out = u[["USUBJID"]].copy()
out["TRTDURD"] = (e - s).dt.days
out.to_parquet("/work/out/result.parquet", index=False)
