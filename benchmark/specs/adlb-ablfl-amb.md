# ADLB: ABLFL (baseline record flag)

Derive `ABLFL` for the lab results in `lb_upstream`: for each subject and parameter (`PARAMCD`), flag with `Y` the baseline record, which is the last non-missing result before the subject's first dose date `TRTSDT`. Other records are missing (null).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
