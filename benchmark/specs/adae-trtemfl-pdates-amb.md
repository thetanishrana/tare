# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`, which holds the analysis start date `ASTDT` (a start date given only as a month or year has been filled in to a full date, and `ASTDTF` says so; `ASTDT` is missing when the event has no start date), the AE end date `AENDT`, and the first and last dose dates `TRTSDT` and `TRTEDT`. An AE is treatment-emergent (`Y`) if it starts after the first dose and no more than 30 days after the last dose. Otherwise `TRTEMFL` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
