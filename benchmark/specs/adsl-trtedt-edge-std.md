# ADSL: TRTEDT (treatment end date)

Derive `TRTEDT`, the date each subject received their last study treatment.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

Only records whose end date `EXENDTC` is a complete date (year, month and day all present) can be used; a record with a partial or missing end date is ignored (the start date is not used as a substitute).

`TRTEDT` is the latest `EXENDTC` date among the subject's usable qualifying records. A subject with no usable qualifying record gets a missing `TRTEDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.
