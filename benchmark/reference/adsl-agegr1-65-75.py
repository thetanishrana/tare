import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


dm = pd.read_parquet("/work/inputs/dm.parquet")


def grp(a):
    if pd.isna(a):
        return "Missing"
    if a < 65:
        return "<65"
    if a <= 74:
        return "65-74"
    return ">=75"


out = dm[["USUBJID"]].copy()
out["AGEGR1"] = dm["AGE"].map(grp)
out.to_parquet("/work/out/result.parquet", index=False)
