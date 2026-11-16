# ADAE: AENDT and AENDTF (analysis end date and imputation flag)

Derive `AENDT`, the analysis end date of each adverse event in `ae`, from the (possibly partial) ISO 8601 end date `AEENDTC`, and `AENDTF`, the flag saying which part was imputed. `adsl_upstream` gives each subject's death date `DTHDT` and study completion date `EOSDT` as dates (either can be missing).

| `AEENDTC` | `AENDT` | `AENDTF` |
|---|---|---|
| complete date | that date | missing (null) |
| year and month only | the **last** day of that month | `D` |
| year only | 31 December of that year | `M` |
| missing or empty | missing (null) | missing (null) |

Ignore any time of day.

**Cap for imputed dates.** Take the earliest of the subject's `DTHDT` and `EOSDT` that are present. If a date was imputed, that earliest date is earlier than the imputed date and it falls inside the period the partial date covers (it is on or after the first day of that month for a year-month date, or of that year for a year-only date), then `AENDT` is that earliest date instead. If the earliest date lies before the period, nothing is adjusted. `AENDTF` is unchanged. Complete dates are never adjusted, and nothing is adjusted when both `DTHDT` and `EOSDT` are missing.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.
