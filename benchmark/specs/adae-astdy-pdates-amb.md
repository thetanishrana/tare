# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` (a start date given only as a month or year has been filled in to a full date, and `ASTDTF` says so; `ASTDT` is missing when the event has no start date) and the subject's first dose date `TRTSDT`. It counts days relative to the first dose. Missing if the start date or the first dose date is missing.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
