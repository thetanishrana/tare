# ADSL: AGEGR1 (sponsor variant: 65 and 75 cut points)

Derive `AGEGR1`, the age group, from `AGE` in `dm` (age in years). This sponsor uses its own cut points.

| Age | `AGEGR1` |
|---|---|
| below 65 | `<65` |
| 65 to 74 inclusive | `65-74` |
| 75 or above | `>=75` |
| missing | `Missing` |

`AGEGR1` is never null; use the text `Missing` when the age is missing.

Write one row for every subject in `dm`, including subjects who never received treatment.
