# ADAE: ASTDT and ASTDTF (analysis start date and imputation flag)

Derive `ASTDT`, the analysis start date of each adverse event in `ae`, from the (possibly partial) ISO 8601 start date `AESTDTC`, and `ASTDTF`, the imputation flag: `D` when the day was imputed, `M` when the month was imputed (and the day), and missing when nothing was imputed. Impute missing parts to the earliest possible date, but do not put an imputed start before the subject's first dose date `TRTSDT` (from `adsl_upstream`) when the event could have started on or after it. Ignore time of day.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.
