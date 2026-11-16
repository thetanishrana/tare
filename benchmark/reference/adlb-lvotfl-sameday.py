import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
t = u[u["ONTRTFL"] == "Y"].copy()
t["d"] = pd.to_datetime(t["ADT"])
t = t.sort_values(["USUBJID", "PARAMCD", "d", "AVAL"], na_position="last")
last = t.groupby(["USUBJID", "PARAMCD"]).tail(1).index
out = u[["USUBJID", "LBSEQ"]].copy()
out["LVOTFL"] = None
out.loc[last, "LVOTFL"] = "Y"
out.to_parquet("/work/out/result.parquet", index=False)
