# ADSL: EOSSTT (end-of-study status)

Derive `EOSSTT`, the end-of-study status, from the disposition records in `ds`.

Use only rows of `ds` where `DSCAT` is `DISPOSITION EVENT`. A subject has at most one such row. Look at its `DSDECOD`:

| Situation | `EOSSTT` |
|---|---|
| `DSDECOD` is `COMPLETED` | `COMPLETED` |
| `DSDECOD` is `SCREEN FAILURE` | missing (null): screen failures have no study status |
| any other `DSDECOD` | `DISCONTINUED` |
| the subject has no such row | `ONGOING` |

Write one row for every subject in `dm`, including subjects who never received treatment.
