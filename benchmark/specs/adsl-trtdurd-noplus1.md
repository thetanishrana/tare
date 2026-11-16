# ADSL: TRTDURD (sponsor variant: elapsed days)

Derive `TRTDURD`, the treatment duration in days, from the treatment start date `TRTSDT` and end date `TRTEDT` in `adsl_upstream`.

This sponsor reports elapsed days, not inclusive days: `TRTDURD` is `TRTEDT` minus `TRTSDT` in days, with **no** extra day added. A subject whose start and end fall on the same day has a duration of 0.

If either date is missing, `TRTDURD` is missing.

Write one row per row of `adsl_upstream` (one per subject).
