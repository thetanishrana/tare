import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
ok = u["AVAL"].notna() & u["BASE"].notna() & (u["BASE"] != 0)
r = (u["AVAL"] / u["BASE"]).where(ok)
r = r.mask((u["AVAL"] == 0) & (u["BASE"] == 0), 1.0)
out = u[["USUBJID", "LBSEQ"]].copy()
out["R2BASE"] = r
out.to_parquet("/work/out/result.parquet", index=False)
