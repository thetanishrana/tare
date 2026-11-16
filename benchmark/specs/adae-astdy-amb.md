# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` and the subject's first dose date `TRTSDT`. It counts days relative to the first dose. Missing if either date is missing.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
