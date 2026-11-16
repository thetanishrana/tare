# ADSL: disposition dates (RANDDT, FRVDT, SCRFDT, EOSDT)

`ds` holds disposition and milestone records, one row per record, with the category `DSCAT`, the term `DSDECOD` and the start date `DSSTDTC` (a complete date). Derive four dates for every subject in `dm`: the randomization date `RANDDT`, the final retrieval visit date `FRVDT`, the screen failure date `SCRFDT` and the end-of-study date `EOSDT`, each taken from the matching disposition record. A date is missing when the subject has no such record.

Write one row for every subject in `dm`, including subjects who never received treatment.
