# ADVS: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the vital-sign measurements in `advs_upstream`: `Y` for measurements taken during treatment, that is between the subject's first dose date `TRTSDT` and last dose date `TRTEDT`; missing (null) otherwise. `ADT` is the measurement date and `AVISIT` the analysis visit name.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
