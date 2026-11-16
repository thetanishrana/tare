# ADAE: ADURN (adverse event duration in days)

Derive `ADURN`, the duration of each adverse event in days, from the start date `ASTDT` and end date `AENDT` in `adae_upstream`.

The duration counts both the first and the last day: `AENDT` minus `ASTDT` in days, plus 1. An event that starts and ends on the same day lasts 1 day.

If `AENDT` or `ASTDT` is missing (for instance an event that is still ongoing), `ADURN` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
