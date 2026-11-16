# ADLB: R2BASE (ratio to baseline)

`lb_upstream` has one row per laboratory result: the subject `USUBJID`, the sequence number `LBSEQ` (unique within a subject), the parameter `PARAMCD`, the analysis visit number `AVISITN`, the result `AVAL` (some are missing) and the subject's baseline value for that parameter `BASE` (missing when the subject has no baseline).

Derive `R2BASE`, each result expressed relative to the subject's baseline value for the parameter: `AVAL` compared with `BASE`.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
