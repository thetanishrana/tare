# ADLB: SHIFT1 (shift from the baseline range category)

`lb_upstream` has one row per lab result: the subject `USUBJID`, the sequence number `LBSEQ`, the parameter `PARAMCD`, the baseline flag `ABLFL` (`Y` on each subject-parameter's baseline record, otherwise missing) and the reference range indicator `ANRIND` (`LOW`, `NORMAL`, `HIGH`, or missing).

Derive `SHIFT1`, describing how the reference range category of each result has shifted from the subject's baseline category for the same parameter, written like `NORMAL to HIGH`.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
