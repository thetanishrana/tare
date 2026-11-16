import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
a = pd.to_datetime(u["ADT"])
s = pd.to_datetime(u["TRTSDT"])
e = pd.to_datetime(u["TRTEDT"])
on = (a > s) & (e.isna() | (a < e)) & ~((u["AVISIT"] == "Baseline") & (a == s))
out = u[["USUBJID", "LBSEQ"]].copy()
out["ONTRTFL"] = on.map({True: "Y", False: None})
out.to_parquet("/work/out/result.parquet", index=False)
