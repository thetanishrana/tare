# ADLB: ANRIND (reference range indicator)

Derive `ANRIND`, which says where each lab result lies against the normal range, for the results in `lb_upstream`. `AVAL` is the result, `ANRLO` the lower limit of the normal range and `ANRHI` the upper limit; either limit can be missing.

- `LOW` if `ANRLO` is present and `AVAL` is below it;
- `HIGH` if `ANRHI` is present and `AVAL` is above it;
- otherwise `NORMAL`. A result equal to a limit is `NORMAL`.

`ANRIND` is missing (null) when `AVAL` is missing, and when both `ANRLO` and `ANRHI` are missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
