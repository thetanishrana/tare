# ADVS: ABLFL (baseline flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (for blood pressure and pulse the position and wait, for example `AFTER LYING DOWN FOR 5 MINUTES`; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `ABLFL`, the baseline flag: `Y` on the baseline measurement, the last non-missing measurement of each parameter before the first dose. Other records are missing (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
