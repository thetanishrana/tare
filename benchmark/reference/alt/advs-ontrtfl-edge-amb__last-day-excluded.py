import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
s = pd.to_datetime(u["TRTSDT"])
e = pd.to_datetime(u["TRTEDT"])
flag = (adt >= s) & (e.isna() | (adt < e)) & ~((u["AVISIT"] == "Baseline") & (adt == s))
out = u[["USUBJID", "VSSEQ"]].copy()
out["ONTRTFL"] = ["Y" if f else None for f in flag]
out.to_parquet("/work/out/result.parquet", index=False)
