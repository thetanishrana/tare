import pandas as pd

u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
a = pd.to_datetime(u["ASTDT"])
s = pd.to_datetime(u["TRTSDT"])
e = pd.to_datetime(u["TRTEDT"])
n = pd.to_datetime(u["AENDT"])
w = pd.Timedelta(days=30)
flag = (a.notna() & s.notna() & (a > s) & (e.isna() | (a <= e + w))) | (
    a.isna() & s.notna() & (n.isna() | (n >= s))
)
out = u[["USUBJID", "AESEQ"]].copy()
out["TRTEMFL"] = flag.map({True: "Y", False: None})
out.to_parquet("/work/out/result.parquet", index=False)
