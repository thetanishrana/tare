# ADAE: LDOSEDTM and DOSEON (last dose before an event, and the dose in effect)

For each adverse event in `ae_upstream` (which gives its start date `ASTDT`), derive `LDOSEDTM`, the date of the last dose on or before the event start, and `DOSEON`, the dose in effect on the event start date. Use the exposure records in `ex`.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or `EXDOSE` equals 0 and `EXTRT` contains `PLACEBO`, and whose start date `EXSTDTC` is a complete date. Ignore all other rows. All dosing is once daily.

**`LDOSEDTM`.** A qualifying record that also has a complete end date `EXENDTC` represents one dose on every calendar day from its start date to its end date, both included. `LDOSEDTM` is the latest such dosing day that is on or before `ASTDT`, written as a date (time of day is not collected). Records without a complete end date are not used for `LDOSEDTM`. If there is no such day, `LDOSEDTM` is missing (null).

**`DOSEON`.** Among the subject's qualifying records that have started on or before `ASTDT` and that either end on or after `ASTDT` or have no end date at all (still open), take the one with the latest start date. `DOSEON` is its `EXDOSE`. If there is no such record, `DOSEON` is missing (null).

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.
