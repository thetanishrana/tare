# ADVS: summary records (the average of repeated readings)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the parameter `PARAMCD`, the measurement date `ADT`, the analysis visit `AVISIT` (the text `(none)` when the measurement belongs to no analysis visit), the time point `ATPT` and the result `AVAL` (a few results are missing).

Derive the summary records: for each subject, parameter and visit, one row holding the average of the readings taken then.

Write one row per summary record, with the columns `USUBJID`, `PARAMCD`, `ADT`, `AVISIT` and `AVAL`.
