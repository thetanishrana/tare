# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` and the subject's first dose date `TRTSDT`.

Study days have no day 0. The first dose day is study day 1, the day before it is study day -1, and so on:

- if `ASTDT` is on or after `TRTSDT`: `ASTDY` is `ASTDT` minus `TRTSDT` in days, plus 1;
- if `ASTDT` is before `TRTSDT`: `ASTDY` is `ASTDT` minus `TRTSDT` in days (a negative number).

If either date is missing, `ASTDY` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
