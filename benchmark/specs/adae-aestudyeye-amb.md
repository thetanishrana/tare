# ADAE: AESTEFL (adverse event in the study eye)

`ae_upstream` holds one row per adverse event: `AELAT` is the eye the event affected (`LEFT`, `RIGHT` or `BOTH`; missing for events that are not eye events) and `STUDYEYE` the subject's study eye (`LEFT` or `RIGHT`).

Derive `AESTEFL`, which marks the adverse events that occurred in the study eye.

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.
