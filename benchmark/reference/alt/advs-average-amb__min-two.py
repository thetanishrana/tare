import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
g = (
    u.dropna(subset=["AVAL"])
    .groupby(["USUBJID", "PARAMCD", "ADT", "AVISIT"])["AVAL"]
    .agg(["mean", "count"])
    .reset_index()
    .query("count >= 2")
    .rename(columns={"mean": "AVAL"})
    .drop(columns="count")
)
g.to_parquet("/work/out/result.parquet", index=False)
