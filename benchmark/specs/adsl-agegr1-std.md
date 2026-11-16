# ADSL: AGEGR1 (age group)

Derive `AGEGR1`, the age group, from `AGE` in `dm` (age in years).

| Age | `AGEGR1` |
|---|---|
| below 18 | `<18` |
| 18 to 64 inclusive | `18-64` |
| above 64 | `>64` |
| missing | `Missing` |

`AGEGR1` is never null; use the text `Missing` when the age is missing.

Write one row for every subject in `dm`, including subjects who never received treatment.
