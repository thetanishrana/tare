import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
a = pd.to_datetime(u["ASTDT"])
s = pd.to_datetime(u["TRTSDT"])
e = pd.to_datetime(u["TRTEDT"])
flag = a.notna() & s.notna() & (a >= s) & (e.isna() | (a <= e + pd.Timedelta(days=0)))
out = u[["USUBJID", "AESEQ"]].copy()
out["TRTEMFL"] = flag.map({True: "Y", False: None})
out.to_parquet("/work/out/result.parquet", index=False)
