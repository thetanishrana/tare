import pandas as pd

u = pd.read_parquet("/work/inputs/oe_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
trt = pd.to_datetime(u["TRTSDT"])
c = u[
    u["AVAL"].notna() & adt.notna() & trt.notna() & (adt <= trt) & (u["OETPT"] == "PRE-DOSE")
].copy()
c["_adt"] = adt[c.index]
c = c.sort_values(["USUBJID", "PARAMCD", "OELAT", "_adt", "OESEQ"])
base = (
    c.groupby(["USUBJID", "PARAMCD", "OELAT"])
    .tail(1)
    .set_index(["USUBJID", "PARAMCD", "OELAT"])["AVAL"]
)
b = pd.Series(list(zip(u["USUBJID"], u["PARAMCD"], u["OELAT"]))).map(base)
post = adt.notna() & trt.notna() & (adt > trt)
out = u[["USUBJID", "OESEQ"]].copy()
out["CHG"] = (u["AVAL"].reset_index(drop=True) - b).where(post.reset_index(drop=True)).values
out.to_parquet("/work/out/result.parquet", index=False)
