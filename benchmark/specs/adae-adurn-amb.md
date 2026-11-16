# ADAE: ADURN (adverse event duration in days)

Derive `ADURN`, how long each adverse event lasted in days, from the start date `ASTDT` and end date `AENDT` in `adae_upstream`. Missing if the duration cannot be determined.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
