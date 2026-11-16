# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`, which holds the analysis start date `ASTDT` and the first and last dose dates `TRTSDT` and `TRTEDT`. An AE is treatment-emergent (`Y`) if it starts after the first dose and no more than 30 days after the last dose. Otherwise `TRTEMFL` is missing (null).

Write one row per row of `adae_upstream`.
