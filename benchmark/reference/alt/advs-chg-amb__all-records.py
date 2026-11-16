import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
trt = pd.to_datetime(u["TRTSDT"])
atpt = u["ATPT"].fillna("(none)")
c = u[u["AVAL"].notna() & adt.notna() & trt.notna() & (adt <= trt)].copy()
c["_adt"], c["_atpt"] = adt[c.index], atpt[c.index]
c = c.sort_values(["USUBJID", "PARAMCD", "_atpt", "_adt", "VISITNUM", "VSSEQ"])
base = (
    c.groupby(["USUBJID", "PARAMCD", "_atpt"])
    .tail(1)
    .set_index(["USUBJID", "PARAMCD", "_atpt"])["AVAL"]
)
b = pd.Series(
    [base.get(k) for k in zip(u["USUBJID"], u["PARAMCD"], atpt)], index=u.index, dtype=float
)
out = u[["USUBJID", "VSSEQ"]].copy()
out["CHG"] = u["AVAL"] - b
out.to_parquet("/work/out/result.parquet", index=False)
