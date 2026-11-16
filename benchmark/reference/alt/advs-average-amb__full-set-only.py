import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet").dropna(subset=["AVAL"])
g = u.groupby(["USUBJID", "PARAMCD", "ADT", "AVISIT"])["AVAL"].agg(["mean", "count"]).reset_index()
g = g[g["count"] == g.groupby("PARAMCD")["count"].transform("max")]
g = g.rename(columns={"mean": "AVAL"}).drop(columns="count")
g.to_parquet("/work/out/result.parquet", index=False)
