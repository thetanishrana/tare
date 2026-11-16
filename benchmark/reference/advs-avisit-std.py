import pandas as pd

u = pd.read_parquet("/work/inputs/advs_upstream.parquet")
title = u["VISIT"].str.title()
drop = u["VISIT"].str.contains("SCREEN|UNSCHED|RETRIEVAL|AMBUL")
av = title.where(~drop)
out = u[["USUBJID", "VSSEQ"]].copy()
out["AVISIT"] = av
out.to_parquet("/work/out/result.parquet", index=False)
