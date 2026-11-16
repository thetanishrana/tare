import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
ok = u["AVAL"].notna() & u["BASE"].notna() & (u["BASE"] != 0)
out = u[["USUBJID", "LBSEQ"]].copy()
out["PCHG"] = (100 * (u["AVAL"] - u["BASE"]) / u["BASE"]).where(ok)
out.to_parquet("/work/out/result.parquet", index=False)
