# ADAE: LDOSEDTM and DOSEON (last dose before an event, and the dose in effect)

For each adverse event in `ae_upstream` (which gives its start date `ASTDT`), derive `LDOSEDTM`, the date of the last dose on or before the event start, and `DOSEON`, the dose in effect on the event start date. Use the exposure records in `ex`, where an exposure record covers a period from its start date `EXSTDTC` to its end date `EXENDTC`. Ignore records that did not give study treatment.

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.
