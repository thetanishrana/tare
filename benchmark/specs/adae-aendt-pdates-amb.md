# ADAE: AENDT and AENDTF (analysis end date and imputation flag)

Derive `AENDT`, the analysis end date of each adverse event in `ae`, from the (possibly partial) ISO 8601 end date `AEENDTC`, and `AENDTF`, the imputation flag: `D` when the day was imputed, `M` when the month and day were imputed, missing when nothing was imputed. Fill in the missing parts of a partial date; a missing end date stays missing. `adsl_upstream` gives each subject's death date `DTHDT` and study completion date `EOSDT` as dates (either can be missing). Ignore any time of day.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.
