import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
adt = pd.to_datetime(u["ADT"])
trt = pd.to_datetime(u["TRTSDT"])
cand = u[u["AVAL"].notna() & adt.notna() & trt.notna() & (adt <= trt)].copy()
cand["_adt"] = adt[cand.index]
cand = cand.sort_values(["USUBJID", "PARAMCD", "VISITNUM", "_adt", "LBSEQ"])
last = cand.groupby(["USUBJID", "PARAMCD"]).tail(1)
out = u[["USUBJID", "LBSEQ"]].copy()
out["ABLFL"] = None
out.loc[last.index, "ABLFL"] = "Y"
out.to_parquet("/work/out/result.parquet", index=False)
