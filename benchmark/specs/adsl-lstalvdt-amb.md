# ADSL: LSTALVDT (last known alive date)

Derive `LSTALVDT`, the last date the subject is known to have been alive, as the latest date on which the subject has a dated record in the study data. The datasets provided are `ae`, `lb`, `vs` and `adsl_upstream` (which holds the treatment end date `TRTEDT`). Missing if there is no usable date.

Write one row for every subject in `dm`.
