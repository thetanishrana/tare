# ADSL: TRTDURD (treatment duration)

Derive `TRTDURD`, the number of days each subject was on treatment, from the treatment start date `TRTSDT` and end date `TRTEDT` in `adsl_upstream`. It is missing if either date is missing.

Write one row per row of `adsl_upstream` (one per subject).
