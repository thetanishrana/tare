# ADLB: LVOTFL (last valid on-treatment record)

Derive `LVOTFL`, which flags each subject's last on-treatment result for each parameter, from the lab results in `lb_upstream`. `ADT` is the date of a result, `AVAL` its value and `ONTRTFL` the on-treatment flag (`Y` or missing). Some subjects have repeat results on the same date as another result.

For each subject and each `PARAMCD`, look only at records with `ONTRTFL` equal to `Y` and order them by `ADT`, then by `AVAL`, both ascending. A missing `AVAL` sorts after every value. The **last** record in that order gets `LVOTFL` = `Y`.

`LVOTFL` is missing (null) on every other record, including all records of a subject and parameter that has no on-treatment record.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.
