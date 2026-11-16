# ADLB: PCHG (percent change from baseline)

Derive `PCHG`, the percent change from baseline, for the lab results in `lb_upstream`. `AVAL` is the result, `BASE` the subject's baseline value for that parameter and `AVISITN` the numeric analysis visit (0 is baseline).

For **post-baseline** records only (`AVISITN` greater than 0), `PCHG` is `100 * (AVAL - BASE) / BASE`.

`PCHG` is missing (null) for every other record (baseline, earlier visits), when `AVAL` or `BASE` is missing, and when `BASE` is 0 (no percentage can be formed). Do not round.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
