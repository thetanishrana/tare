import datetime as dt

import pandas as pd

ae = pd.read_parquet("/work/inputs/ae.parquet")
adsl = pd.read_parquet("/work/inputs/adsl_upstream.parquet").set_index("USUBJID")


def impute(dtc, subj):
    if dtc is None or pd.isna(dtc) or dtc == "":
        return None, None
    p = dtc[:10].split("-")
    y = int(p[0])
    if len(p) == 3:
        return dt.date(y, int(p[1]), int(p[2])), None
    if len(p) == 2:
        m = int(p[1])
        _, res, flag = dt.date(y, m, 1), dt.date(y, m, 15), "D"
    else:
        _, res, flag = dt.date(y, 1, 1), dt.date(y, 6, 30), "M"
    return res, flag


rows = []
for subj, seq, dtc in zip(ae["USUBJID"], ae["AESEQ"], ae["AEENDTC"]):
    d, f = impute(dtc, subj)
    rows.append({"USUBJID": subj, "AESEQ": seq, "AENDT": d, "AENDTF": f})
out = pd.DataFrame(rows)
out["AENDT"] = out["AENDT"].astype(object).where(out["AENDT"].notna(), None)
out.to_parquet("/work/out/result.parquet", index=False)
