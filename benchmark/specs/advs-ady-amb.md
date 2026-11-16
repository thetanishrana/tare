# ADVS: ADY (analysis study day)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the measurement date `ADT` and the subject's first dose date `TRTSDT`.

Derive `ADY`, the study day of the measurement relative to the first dose date. `ADY` is missing (null) when `ADT` or `TRTSDT` is missing.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
