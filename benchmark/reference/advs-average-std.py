import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
g = (
    u.dropna(subset=["AVAL"])
    .groupby(["USUBJID", "PARAMCD", "ADT", "AVISIT"], as_index=False)["AVAL"]
    .mean()
)
g.to_parquet("/work/out/result.parquet", index=False)
