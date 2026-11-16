# ADSL: TRTDURD (treatment duration in days)

Derive `TRTDURD`, the treatment duration in days, from the treatment start date `TRTSDT` and end date `TRTEDT` in `adsl_upstream`.

`TRTDURD` counts both the first and the last day of treatment: `TRTEDT` minus `TRTSDT` in days, plus 1. A subject whose start and end fall on the same day has a duration of 1.

If either date is missing, `TRTDURD` is missing.

Write one row per row of `adsl_upstream` (one per subject).
