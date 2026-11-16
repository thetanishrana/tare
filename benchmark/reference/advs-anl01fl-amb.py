import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
u["_atpt"] = u["ATPT"].fillna("(none)")
u["_avisit"] = u["AVISIT"].fillna("(none)")
u["_aval"] = u["AVAL"].fillna(-1e18)
c = u[(u["ONTRTFL"] == "Y") & u["AVISITN"].notna()]
last = (
    c.sort_values(["ADT", "_aval", "VSSEQ"])
    .groupby(["USUBJID", "PARAMCD", "_avisit", "_atpt"])
    .tail(1)
)
out = u[["USUBJID", "VSSEQ"]].copy()
out["ANL01FL"] = None
out.loc[last.index, "ANL01FL"] = "Y"
out.to_parquet("/work/out/result.parquet", index=False)
