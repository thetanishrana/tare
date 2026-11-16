import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
d = (pd.to_datetime(u["ADT"]) - pd.to_datetime(u["TRTSDT"])).dt.days
ady = d
out = u[["USUBJID", "VSSEQ"]].copy()
out["ADY"] = ady
out.to_parquet("/work/out/result.parquet", index=False)
