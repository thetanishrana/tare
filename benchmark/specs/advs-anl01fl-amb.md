# ADVS: ANL01FL (analysis record flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (missing for parameters measured once per visit), the analysis visit name `AVISIT` and number `AVISITN` (both missing for measurements that fall outside the scheduled visits), the measurement date `ADT`, the result `AVAL` (a few are missing) and the on-treatment flag `ONTRTFL` (`Y` or missing).

Derive `ANL01FL`, the analysis record flag: `Y` on the record used for analysis, the last measurement of each subject, parameter and analysis visit; missing (null) on all other records.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
