# ADVS: summary records (the average of repeated readings)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the parameter `PARAMCD`, the measurement date `ADT`, the analysis visit `AVISIT` (the text `(none)` when the measurement belongs to no analysis visit, for example screening or unscheduled measurements), the time point `ATPT` and the result `AVAL` (a few results are missing).

Derive the summary records. For every distinct combination of `USUBJID`, `PARAMCD`, `ADT` and `AVISIT`, write one row whose `AVAL` is the arithmetic mean of the non-missing `AVAL` values in that combination. Do not round. A combination that has a single non-missing result still gets a row (its mean is that result). A combination with no non-missing result gets no row.

Write one row per combination, with the columns `USUBJID`, `PARAMCD`, `ADT`, `AVISIT` and `AVAL`.
