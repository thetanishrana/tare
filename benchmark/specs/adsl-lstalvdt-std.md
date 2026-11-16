# ADSL: LSTALVDT (last known alive date)

Derive `LSTALVDT`, the last date the subject is known to have been alive: the **latest** of these dates for the subject.

- AE start dates (`AESTDTC` in `ae`)
- AE end dates (`AEENDTC` in `ae`)
- lab sample dates (`LBDTC` in `lb`)
- the treatment end date `TRTEDT` (from `adsl_upstream`, already a date)

Dates in `ae`, `lb` are ISO 8601 text. Convert each to a calendar date as follows: ignore any time of day; if only the year and month are present use the first day of that month; if only the year is present use 1 January of that year; skip empty or missing values.

A subject with no usable date from any source gets a missing `LSTALVDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.
