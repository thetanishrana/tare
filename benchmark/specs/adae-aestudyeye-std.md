# ADAE: AESTEFL (adverse event in the study eye)

`ae_upstream` holds one row per adverse event: `AELAT` is the eye the event affected (`LEFT`, `RIGHT` or `BOTH`; missing for events that are not eye events) and `STUDYEYE` the subject's study eye (`LEFT` or `RIGHT`).

Derive `AESTEFL`:

- missing (null) when `AELAT` is missing (the event is not an eye event);
- `Y` when `AELAT` is `BOTH`, or equals `STUDYEYE`;
- `N` when `AELAT` is the other eye (not the study eye).

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.
