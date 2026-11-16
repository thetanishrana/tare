# ADLB: CHG (sponsor variant: on-treatment records only)

Derive `CHG`, the change from baseline, for the lab results in `lb_upstream`. `AVAL` is the result, `BASE` the subject's baseline value for that parameter, `AVISITN` the numeric analysis visit (0 is baseline), and `ONTRTFL` the on-treatment flag (`Y` or missing).

This sponsor reports change only for post-baseline results taken on treatment. `CHG` is `AVAL` minus `BASE` for records where **both** `AVISITN` is greater than 0 **and** `ONTRTFL` is `Y`. For every other record `CHG` is missing (null). `CHG` is also missing if `AVAL` or `BASE` is missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
