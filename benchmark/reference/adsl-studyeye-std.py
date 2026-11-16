import pandas as pd

dm = pd.read_parquet("/work/inputs/dm.parquet")
sc = pd.read_parquet("/work/inputs/sc_ophtha.parquet")
f = (
    sc[sc["SCTESTCD"] == "FOCID"]
    .drop_duplicates("USUBJID")
    .set_index("USUBJID")["SCSTRESC"]
    .map({"OD": "RIGHT", "OS": "LEFT"})
)
out = dm[["USUBJID"]].copy()
out["STUDYEYE"] = out["USUBJID"].map(f)
out.to_parquet("/work/out/result.parquet", index=False)
