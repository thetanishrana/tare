import pandas as pd

u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
d = (pd.to_datetime(u["ASTDT"]) - pd.to_datetime(u["TRTSDT"])).dt.days
y = d + 1
out = u[["USUBJID", "AESEQ"]].copy()
out["ASTDY"] = y
out.to_parquet("/work/out/result.parquet", index=False)
