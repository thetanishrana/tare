# ADSL: SAFFL (safety population flag)

Derive `SAFFL`, the safety population flag.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

`SAFFL` is `Y` for a subject with at least one qualifying exposure record, and `N` otherwise. It is never missing.

Write one row for every subject in `dm`, including subjects who never received treatment.
