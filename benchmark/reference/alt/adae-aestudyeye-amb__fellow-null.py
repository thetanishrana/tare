import pandas as pd

u = pd.read_parquet("/work/inputs/ae_upstream.parquet")
lat, se = u["AELAT"], u["STUDYEYE"]
flag = pd.Series(None, index=u.index, dtype=object)
flag[lat.notna() & ((lat == "BOTH") | (lat == se))] = "Y"
out = u[["USUBJID", "AESEQ"]].copy()
out["AESTEFL"] = flag
out.to_parquet("/work/out/result.parquet", index=False)
