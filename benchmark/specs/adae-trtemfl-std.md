# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`. It already holds the analysis start date `ASTDT`, the first dose date `TRTSDT` and the last dose date `TRTEDT` as dates. (The AE end date `AENDT` is present but is not used.)

An AE is treatment-emergent (`TRTEMFL` = `Y`) when both hold:

1. it started on or after the first dose date: `ASTDT` is on or after `TRTSDT`; and
2. it started no later than **30 days after** the last dose date: `ASTDT` is on or before `TRTEDT` plus 30 days (the 30th day is included). If `TRTEDT` is missing there is no upper limit.

If `ASTDT` or `TRTSDT` is missing, the flag is not set. In every case where the flag is not `Y`, `TRTEMFL` is missing (null), not `N`.

Write one row per row of `adae_upstream`.
