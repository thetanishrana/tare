# ADVS: AVISIT (analysis visit)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the visit name as collected `VISIT` (capital letters, for example `BASELINE` or `WEEK 12`) and the visit number `VISITNUM`.

Derive `AVISIT`, the analysis visit name:

- a `VISIT` containing any of the texts `SCREEN`, `UNSCHED`, `RETRIEVAL` or `AMBUL` is not an analysis visit: `AVISIT` is missing (null);
- every other `VISIT` becomes its text in title case (first letter of each word capital, the rest lower case), so `BASELINE` gives `Baseline` and `WEEK 12` gives `Week 12`.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
