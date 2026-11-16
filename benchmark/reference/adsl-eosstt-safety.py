import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


dm = pd.read_parquet("/work/inputs/dm.parquet")
ds = pd.read_parquet("/work/inputs/ds.parquet")
d = ds[ds["DSCAT"] == "DISPOSITION EVENT"].set_index("USUBJID")["DSDECOD"]


def status(subj):
    if subj not in d.index:
        return "ONGOING"
    x = d[subj]
    if x == "COMPLETED":
        return "COMPLETED"
    if x == "SCREEN FAILURE":
        return None
    if x in ("ADVERSE EVENT", "DEATH"):
        return "DISCONTINUED - SAFETY"
    return "DISCONTINUED - OTHER"


out = dm[["USUBJID"]].copy()
out["EOSSTT"] = out["USUBJID"].map(status)
out.to_parquet("/work/out/result.parquet", index=False)
