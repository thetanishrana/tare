import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
bl = (
    u[u["ABLFL"] == "Y"]
    .drop_duplicates(["USUBJID", "PARAMCD"])
    .set_index(["USUBJID", "PARAMCD"])["ANRIND"]
)
b = pd.Series([bl.get(k) for k in zip(u["USUBJID"], u["PARAMCD"])], index=u.index).fillna("NULL")
a = u["ANRIND"].fillna("NULL")
out = u[["USUBJID", "LBSEQ"]].copy()
out["SHIFT1"] = (b + " to " + a).where(u["ABLFL"] != "Y")
out.to_parquet("/work/out/result.parquet", index=False)
