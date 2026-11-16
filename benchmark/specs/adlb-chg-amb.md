# ADLB: CHG (change from baseline)

Derive `CHG`, the change from baseline, for the lab results in `lb_upstream`: the result `AVAL` minus the subject's baseline value `BASE` for that parameter. `AVISITN` is the numeric analysis visit (0 is baseline).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
