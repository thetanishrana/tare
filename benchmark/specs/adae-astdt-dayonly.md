# ADAE: ASTDT and ASTDTF (sponsor variant: only a missing day is imputed)

Derive `ASTDT`, the analysis start date of each adverse event in `ae`, from the (possibly partial) ISO 8601 start date `AESTDTC`, and `ASTDTF`, the flag saying which part was imputed. This sponsor imputes **only a missing day**, never a missing month or year.

| `AESTDTC` | `ASTDT` | `ASTDTF` |
|---|---|---|
| complete date | that date | missing (null) |
| year and month only | the **15th** day of that month | `D` |
| year only | missing (null): no imputation | missing (null) |
| missing or empty | missing (null) | missing (null) |

Ignore any time of day.

**First-dose adjustment.** `adsl_upstream` gives each subject's first dose date `TRTSDT`. If a year-month date was imputed to the 15th, the imputed date is earlier than `TRTSDT`, and `TRTSDT` lies in that same month, then `ASTDT` is `TRTSDT` instead: the event may have started on the first dose day. `ASTDTF` is unchanged. Complete dates are never adjusted, and nothing is adjusted when `TRTSDT` is missing.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.
