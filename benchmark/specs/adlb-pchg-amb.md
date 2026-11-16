# ADLB: PCHG (percent change from baseline)

Derive `PCHG`, the percent change from baseline, for the lab results in `lb_upstream`: the change of the result `AVAL` from the subject's baseline value `BASE`, expressed as a percentage of the baseline. `AVISITN` is the numeric analysis visit (0 is baseline).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
