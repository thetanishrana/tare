# ADSL: disposition dates (RANDDT, FRVDT, SCRFDT, EOSDT)

`ds` holds disposition and milestone records, one row per record, with the category `DSCAT`, the term `DSDECOD` and the start date `DSSTDTC` (a complete date). Derive four dates for every subject in `dm`:

- `RANDDT`, the randomization date: `DSSTDTC` of the subject's record whose `DSDECOD` is `RANDOMIZED`.
- `FRVDT`, the final retrieval visit date: `DSSTDTC` of the record whose `DSDECOD` is `FINAL RETRIEVAL VISIT`.
- `SCRFDT`, the screen failure date: `DSSTDTC` of the record whose `DSCAT` is `DISPOSITION EVENT` and whose `DSDECOD` is `SCREEN FAILURE`.
- `EOSDT`, the end-of-study date: `DSSTDTC` of the record whose `DSCAT` is `DISPOSITION EVENT`, **except** that a screen failure has no end-of-study date (their disposition date is `SCRFDT`).

A date is missing (null) when the subject has no such record. A subject has at most one record of each kind.

Write one row for every subject in `dm`, including subjects who never received treatment.
