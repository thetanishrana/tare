# ADSL: EOSSTT (sponsor variant: safety discontinuations)

Derive `EOSSTT`, the end-of-study status, from the disposition records in `ds`. This sponsor separates safety-related discontinuations from the rest.

Use only rows of `ds` where `DSCAT` is `DISPOSITION EVENT`. A subject has at most one such row. Look at its `DSDECOD`:

| Situation | `EOSSTT` |
|---|---|
| `DSDECOD` is `COMPLETED` | `COMPLETED` |
| `DSDECOD` is `SCREEN FAILURE` | missing (null): screen failures have no study status |
| `DSDECOD` is `ADVERSE EVENT` or `DEATH` | `DISCONTINUED - SAFETY` |
| any other `DSDECOD` | `DISCONTINUED - OTHER` |
| the subject has no such row | `ONGOING` |

Write one row for every subject in `dm`, including subjects who never received treatment.
