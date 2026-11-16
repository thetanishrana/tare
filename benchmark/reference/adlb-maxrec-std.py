import pandas as pd

u = pd.read_parquet("/work/inputs/lb_upstream.parquet")
q = u[u["AVAL"].notna() & (u["ONTRTFL"] == "Y")].copy()
q["d"] = pd.to_datetime(q["ADT"])
q = q.sort_values(
    ["USUBJID", "PARAMCD", "AVAL", "d", "AVISITN"], ascending=[True, True, False, True, True]
)
out = q.groupby(["USUBJID", "PARAMCD"], as_index=False).head(1)[
    ["USUBJID", "PARAMCD", "LBSEQ", "AVAL", "ADT"]
]
out.to_parquet("/work/out/result.parquet", index=False)
