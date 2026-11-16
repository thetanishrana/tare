# ADVS: CHG (change from baseline)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (position and wait for blood pressure and pulse; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the analysis visit number `AVISITN` (0 is the baseline visit; screening and unscheduled records have none), the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `CHG`, the change from baseline: the result `AVAL` minus the subject's baseline value for the parameter, where the baseline is the last non-missing measurement on or before the first dose date.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
