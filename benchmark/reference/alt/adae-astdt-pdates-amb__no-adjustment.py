import pandas as pd


def to_date(series):
    return [d.date() if pd.notna(d) else None for d in series]


import datetime as dt

ae = pd.read_parquet("/work/inputs/ae.parquet")
adsl = pd.read_parquet("/work/inputs/adsl_upstream.parquet").set_index("USUBJID")["TRTSDT"]


def impute(dtc, trtsdt):
    if dtc is None or pd.isna(dtc) or dtc == "":
        return None, None
    p = dtc[:10].split("-")
    y = int(p[0])
    if len(p) == 3:
        return dt.date(y, int(p[1]), int(p[2])), None
    if len(p) == 2:
        m, flag = int(p[1]), "D"
        d = 1
        res = dt.date(y, m, d)
    else:
        m, flag = 1, "M"
        res = dt.date(y, 1, 1)
    if False:
        res = trtsdt
    return res, flag


rows = []
for subj, seq, dtc in zip(ae["USUBJID"], ae["AESEQ"], ae["AESTDTC"]):
    d, f = impute(dtc, adsl.get(subj))
    rows.append({"USUBJID": subj, "AESEQ": seq, "ASTDT": d, "ASTDTF": f})
out = pd.DataFrame(rows)
out["ASTDT"] = out["ASTDT"].astype(object).where(out["ASTDT"].notna(), None)
out.to_parquet("/work/out/result.parquet", index=False)
