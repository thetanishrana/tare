# ADLB: ANRIND (reference range indicator)

Derive `ANRIND`, which says where each lab result lies against the normal range, for the results in `lb_upstream`. `AVAL` is the result, `ANRLO` the lower limit of the normal range and `ANRHI` the upper limit. Results below the range are `LOW`, results above it are `HIGH`, and the rest are `NORMAL`.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
