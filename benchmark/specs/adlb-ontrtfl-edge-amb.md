# ADLB: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the lab results in `lb_upstream`: `Y` for results taken during treatment, that is between the subject's first dose date `TRTSDT` and last dose date `TRTEDT`; missing (null) otherwise. `ADT` is the result date and `AVISIT` the analysis visit name.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
