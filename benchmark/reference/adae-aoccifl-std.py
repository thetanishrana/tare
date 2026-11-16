import pandas as pd

u = pd.read_parquet("/work/inputs/adae_upstream.parquet")
sev = {"MILD": 1, "MODERATE": 2, "SEVERE": 3}
t = u[u["TRTEMFL"] == "Y"].copy()
t["sv"] = t["ASEV"].map(sev)
t["d"] = pd.to_datetime(t["ASTDT"])
t = t.sort_values(["USUBJID", "sv", "d", "AESEQ"], ascending=[True, False, True, True])
chosen = t.groupby("USUBJID").head(1).index
out = u[["USUBJID", "AESEQ"]].copy()
out["AOCCIFL"] = None
out.loc[chosen, "AOCCIFL"] = "Y"
out.to_parquet("/work/out/result.parquet", index=False)
