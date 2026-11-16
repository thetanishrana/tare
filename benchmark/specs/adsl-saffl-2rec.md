# ADSL: SAFFL (sponsor variant: at least two exposure records)

Derive `SAFFL`, the safety population flag.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

This sponsor requires more than a single dose record: `SAFFL` is `Y` for a subject with **at least two** qualifying exposure records (two rows of `ex`, whatever their dates), and `N` otherwise. It is never missing.

Write one row for every subject in `dm`, including subjects who never received treatment.
