# ADVS: ADY (analysis study day)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the measurement date `ADT` and the subject's first dose date `TRTSDT`.

Derive `ADY`, the study day of the measurement relative to the first dose, using the usual clinical-trial convention in which there is no day 0: the first dose day is day 1 and the day before it is day -1. For a measurement on or after the first dose date `ADY` is the number of calendar days from `TRTSDT` to `ADT` plus 1; for a measurement before the first dose date it is the plain difference (a negative number).

`ADY` is missing (null) when `ADT` or `TRTSDT` is missing.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
