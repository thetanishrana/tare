# ADVS: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the vital-sign measurements in `advs_upstream`. `ADT` is the measurement date, `TRTSDT` the subject's first dose date, `TRTEDT` the last dose date and `AVISIT` the analysis visit name.

`ONTRTFL` is `Y` when all of these hold:

1. `ADT` is on or after `TRTSDT`;
2. `TRTEDT` is missing, or `ADT` is on or before `TRTEDT` (the last dose day is included; there is no window after it);
3. it is not a pre-dose measurement: a measurement whose `AVISIT` is `Baseline` and whose `ADT` is the first dose day (`ADT` equals `TRTSDT`) is taken before the first dose, so it is **not** on treatment.

In every case where the flag is not `Y`, `ONTRTFL` is missing (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
