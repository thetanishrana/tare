# ADLB: R2BASE (ratio to baseline)

`lb_upstream` has one row per laboratory result: the subject `USUBJID`, the sequence number `LBSEQ` (unique within a subject), the parameter `PARAMCD`, the analysis visit number `AVISITN`, the result `AVAL` (some are missing) and the subject's baseline value for that parameter `BASE` (missing when the subject has no baseline).

Derive `R2BASE`, the ratio of the result to the baseline: `AVAL` divided by `BASE`, as a plain ratio (1.0 means no change; it is not a percentage and is not rounded). It is derived for every record, baseline and pre-baseline records included.

`R2BASE` is missing (null) when `AVAL` is missing, when `BASE` is missing, or when `BASE` is 0 (a ratio to a zero baseline is not defined, including 0 divided by 0).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
