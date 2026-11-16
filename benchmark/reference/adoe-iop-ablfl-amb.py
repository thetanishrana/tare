import pandas as pd

u = pd.read_parquet("/work/inputs/oe_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
trt = pd.to_datetime(u["TRTSDT"])
c = u[
    u["AVAL"].notna() & adt.notna() & trt.notna() & (adt <= trt) & (u["OETPT"] == "PRE-DOSE")
].copy()
c["_adt"] = adt[c.index]
c = c.sort_values(["USUBJID", "PARAMCD", "OELAT", "_adt", "OESEQ"])
last = c.groupby(["USUBJID", "PARAMCD", "OELAT"]).tail(1)
out = u[["USUBJID", "OESEQ"]].copy()
out["ABLFL"] = None
out.loc[last.index, "ABLFL"] = "Y"
out.to_parquet("/work/out/result.parquet", index=False)
