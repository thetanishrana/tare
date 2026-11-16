import pandas as pd

dm = pd.read_parquet("/work/inputs/dm.parquet")
ds = pd.read_parquet("/work/inputs/ds.parquet")


def pick(mask):
    return (
        ds[mask]
        .drop_duplicates("USUBJID")
        .set_index("USUBJID")["DSSTDTC"]
        .map(lambda s: pd.Timestamp(s).date())
    )


disp = ds["DSCAT"] == "DISPOSITION EVENT"
sf = disp & (ds["DSDECOD"] == "SCREEN FAILURE")
out = dm[["USUBJID"]].copy()
out["RANDDT"] = out["USUBJID"].map(pick(ds["DSDECOD"] == "RANDOMIZED"))
out["FRVDT"] = out["USUBJID"].map(pick(ds["DSDECOD"] == "FINAL RETRIEVAL VISIT"))
out["SCRFDT"] = out["USUBJID"].map(pick(sf))
out["EOSDT"] = out["USUBJID"].map(pick(disp & ~sf))
for c in ("RANDDT", "FRVDT", "SCRFDT", "EOSDT"):
    out[c] = out[c].astype(object).where(out[c].notna(), None)
out.to_parquet("/work/out/result.parquet", index=False)
