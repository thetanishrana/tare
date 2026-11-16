# ADLB: ABLFL (sponsor variant: baseline strictly before first dose)

Derive `ABLFL`, the baseline record flag, for the lab results in `lb_upstream`. `ADT` is the analysis date of each result and `TRTSDT` the subject's first dose date.

This sponsor requires baseline to be **strictly before** the first dose day. For each subject and each `PARAMCD`, the baseline record is the **last** record that:

- has a non-missing `AVAL`, and
- has `ADT` strictly before `TRTSDT` (a result on the first dose day does not count).

"Last" means latest `ADT`; ties on `ADT` are broken by higher `VISITNUM`, and then by higher `LBSEQ`.

`ABLFL` is `Y` on the baseline record. It is missing (null) on every other record, including all records of a subject and parameter that has no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
