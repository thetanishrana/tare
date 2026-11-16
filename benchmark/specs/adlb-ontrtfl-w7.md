# ADLB: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the lab results in `lb_upstream`. `ADT` is the date of each result, `TRTSDT` the subject's first dose date, `TRTEDT` the last dose date and `AVISIT` the analysis visit name.

`ONTRTFL` is `Y` when all of these hold:

1. `ADT` is on or after `TRTSDT`;
2. `TRTEDT` is missing, or `ADT` is on or before `TRTEDT` plus 7 days (the 7th day after the last dose is included);
3. it is not a pre-dose measurement: a result whose `AVISIT` is `Baseline` and whose `ADT` is the first dose day (`ADT` equals `TRTSDT`) is taken before the first dose, so it is **not** on treatment.

In every case where the flag is not `Y`, `ONTRTFL` is missing (null).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
