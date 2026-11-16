# ADVS: CHG (change from baseline, per time point)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (position and wait for blood pressure and pulse; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the analysis visit number `AVISITN` (0 is the baseline visit; screening and unscheduled records have none), the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `CHG`, the change from baseline, in two steps.

1. **Baseline value, per time point.** For each subject, each `PARAMCD` and each value of `ATPT` (a missing `ATPT` is a group of its own), the baseline record is the last record with a non-missing `AVAL` and `ADT` on or before `TRTSDT` (latest `ADT`; ties by the higher `VISITNUM`, then the higher `VSSEQ`). Its `AVAL` is that time point's baseline value; time points are never compared with another time point's baseline.
2. **Change.** For **post-baseline** records only, meaning `AVISITN` greater than 0, `CHG` is `AVAL` minus the baseline value of the same subject, parameter and time point.

`CHG` is missing (null) on every other record (baseline, earlier or unscheduled visits, or a missing `AVISITN`), and whenever `AVAL` is missing or the time point has no baseline record.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
