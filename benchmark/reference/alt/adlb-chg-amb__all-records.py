import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
use = u["AVISITN"] > 0
out = u[["USUBJID", "LBSEQ"]].copy()
out["CHG"] = u["AVAL"] - u["BASE"]
out.to_parquet("/work/out/result.parquet", index=False)
