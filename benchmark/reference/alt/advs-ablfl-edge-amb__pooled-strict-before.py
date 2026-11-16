import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
trt = pd.to_datetime(u["TRTSDT"])
c = u[u["AVAL"].notna() & adt.notna() & trt.notna() & (adt < trt)].copy()
c["_adt"] = adt[c.index]
c["_atpt"] = c["ATPT"].fillna("(none)")
c = c.sort_values(["USUBJID", "PARAMCD", "_adt", "VISITNUM", "VSSEQ"])
last = c.groupby(["USUBJID", "PARAMCD"]).tail(1)
out = u[["USUBJID", "VSSEQ"]].copy()
out["ABLFL"] = None
out.loc[last.index, "ABLFL"] = "Y"
out.to_parquet("/work/out/result.parquet", index=False)
