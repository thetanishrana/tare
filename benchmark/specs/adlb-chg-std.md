# ADLB: CHG (change from baseline)

Derive `CHG`, the change from baseline, for the lab results in `lb_upstream`. `AVAL` is the result, `BASE` the subject's baseline value for that parameter, and `AVISITN` the numeric analysis visit (0 is baseline).

`CHG` is `AVAL` minus `BASE` for **post-baseline** records only, meaning `AVISITN` is greater than 0. For every other record (baseline, earlier visits, or a missing `AVISITN`) `CHG` is missing (null). `CHG` is also missing if `AVAL` or `BASE` is missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
