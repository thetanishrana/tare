import pandas as pd

u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
out = u[["USUBJID", "AESEQ"]].copy()
out["ADURN"] = (pd.to_datetime(u["AENDT"]) - pd.to_datetime(u["ASTDT"])).dt.days
out.to_parquet("/work/out/result.parquet", index=False)
