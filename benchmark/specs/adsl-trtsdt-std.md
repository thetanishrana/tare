# ADSL: TRTSDT (treatment start date)

Derive `TRTSDT`, the date each subject started study treatment.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

Only records whose start date `EXSTDTC` is a complete date (year, month and day all present) can be used; a record with a partial or missing start date is ignored.

`TRTSDT` is the earliest `EXSTDTC` date among the subject's usable qualifying records. A subject with no usable qualifying record gets a missing `TRTSDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.
