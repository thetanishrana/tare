# ADLB: SHIFT1 (shift from the baseline range category)

`lb_upstream` has one row per lab result: the subject `USUBJID`, the sequence number `LBSEQ`, the parameter `PARAMCD`, the baseline flag `ABLFL` (`Y` on each subject-parameter's baseline record, otherwise missing) and the reference range indicator `ANRIND` (`LOW`, `NORMAL`, `HIGH`, or missing).

Derive `SHIFT1`, the text `<baseline category> to <category of this record>`, on every row:

- the baseline category `BNRIND` is the `ANRIND` of the subject's baseline record (`ABLFL` equal to `Y`) for the same `PARAMCD`; it is `NULL` (the word) when the subject has no baseline record for that parameter, or the baseline record's `ANRIND` is missing;
- the category of this record is its own `ANRIND`, or `NULL` (the word) when missing.

For example `NORMAL to HIGH`, `LOW to LOW`, `NULL to NORMAL`. `SHIFT1` is never missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
