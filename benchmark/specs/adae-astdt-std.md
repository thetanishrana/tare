# ADAE: ASTDT and ASTDTF (analysis start date and imputation flag)

Derive `ASTDT`, the analysis start date of each adverse event in `ae`, from the (possibly partial) ISO 8601 start date `AESTDTC`, and `ASTDTF`, the flag saying which part was imputed.

| `AESTDTC` | `ASTDT` | `ASTDTF` |
|---|---|---|
| complete date | that date | missing (null) |
| year and month only | the first day of that month | `D` |
| year only | 1 January of that year | `M` |
| missing or empty | missing (null) | missing (null) |

Ignore any time of day.

**First-dose adjustment.** `adsl_upstream` gives each subject's first dose date `TRTSDT`. If a date was imputed, the imputed date is earlier than `TRTSDT`, and `TRTSDT` lies inside the period the partial date covers (the same month for a year-month date, the same year for a year-only date), then `ASTDT` is `TRTSDT` instead: the event may have started on the first dose day. `ASTDTF` is unchanged. Complete dates are never adjusted, and nothing is adjusted when `TRTSDT` is missing.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.
