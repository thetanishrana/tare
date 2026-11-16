import pandas as pd

u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
a = pd.to_datetime(u["ASTDT"])
s = pd.to_datetime(u["TRTSDT"])
d = (a - s).dt.days
out = u[["USUBJID", "AESEQ"]].copy()
out["ASTDY"] = d.where(d < 0, d + 1)
out.to_parquet("/work/out/result.parquet", index=False)
