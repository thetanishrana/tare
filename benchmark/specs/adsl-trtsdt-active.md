# ADSL: TRTSDT (sponsor variant: first active dose)

Derive `TRTSDT`, the date each subject started **active** treatment.

This sponsor counts only active dosing. A **qualifying exposure record** is a row of `ex` where `EXDOSE` is strictly above 0. Placebo rows (dose 0) do **not** qualify, so a subject who only ever received placebo has no qualifying record. Rows with a missing `EXDOSE` do not qualify.

Only records whose start date `EXSTDTC` is a complete date (year, month and day all present) can be used; a record with a partial or missing start date is ignored.

`TRTSDT` is the earliest `EXSTDTC` date among the subject's usable qualifying records. A subject with no usable qualifying record gets a missing `TRTSDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.
