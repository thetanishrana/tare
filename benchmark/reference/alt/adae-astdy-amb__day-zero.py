import pandas as pd

u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
out = u[["USUBJID", "AESEQ"]].copy()
out["ASTDY"] = (pd.to_datetime(u["ASTDT"]) - pd.to_datetime(u["TRTSDT"])).dt.days
out.to_parquet("/work/out/result.parquet", index=False)
