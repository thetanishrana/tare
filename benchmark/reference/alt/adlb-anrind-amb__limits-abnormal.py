import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
a, lo, hi = u["AVAL"], u["ANRLO"], u["ANRHI"]
ind = pd.Series("NORMAL", index=u.index, dtype=object)
ind[lo.notna() & (a <= lo)] = "LOW"
ind[hi.notna() & (a >= hi)] = "HIGH"
ind[a.isna() | (lo.isna() & hi.isna())] = None
out = u[["USUBJID", "LBSEQ"]].copy()
out["ANRIND"] = ind
out.to_parquet("/work/out/result.parquet", index=False)
