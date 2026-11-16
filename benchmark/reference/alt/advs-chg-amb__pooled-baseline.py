import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
trt = pd.to_datetime(u["TRTSDT"])
atpt = u["ATPT"].fillna("(none)")
c = u[u["AVAL"].notna() & adt.notna() & trt.notna() & (adt <= trt)].copy()
c["_adt"], c["_atpt"] = adt[c.index], atpt[c.index]
c = c.sort_values(["USUBJID", "PARAMCD", "_adt", "VISITNUM", "VSSEQ"])
base = c.groupby(["USUBJID", "PARAMCD"]).tail(1).set_index(["USUBJID", "PARAMCD"])["AVAL"]
b = pd.Series([base.get(k) for k in zip(u["USUBJID"], u["PARAMCD"])], index=u.index, dtype=float)
out = u[["USUBJID", "VSSEQ"]].copy()
out["CHG"] = (u["AVAL"] - b).where(u["AVISITN"] > 0)
out.to_parquet("/work/out/result.parquet", index=False)
