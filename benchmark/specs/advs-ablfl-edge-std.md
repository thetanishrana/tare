# ADVS: ABLFL (baseline flag, separately for each time point)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (for blood pressure and pulse the position and wait, for example `AFTER LYING DOWN FOR 5 MINUTES`; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `ABLFL`, the baseline flag. Baseline is chosen **separately for each time point**: for each subject, each `PARAMCD` and each value of `ATPT` (a missing `ATPT` counts as one group of its own), the baseline record is the **last** record that has a non-missing `AVAL` and `ADT` on or before `TRTSDT`. "Last" means the latest `ADT`; ties are broken by the higher `VISITNUM`, then the higher `VSSEQ`.

`ABLFL` is `Y` on the baseline record and missing (null) on every other record, including all records of a group with no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
