# ADVS: ANL01FL (analysis record flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (missing for parameters measured once per visit), the analysis visit name `AVISIT` and number `AVISITN` (both missing for measurements that fall outside the scheduled visits), the measurement date `ADT`, the result `AVAL` (a few are missing) and the on-treatment flag `ONTRTFL` (`Y` or missing).

Derive `ANL01FL`, the analysis record flag. Only records with `ONTRTFL` equal to `Y` **and** a non-missing `AVISITN` are candidates. Among the candidates, for each subject, `PARAMCD`, `AVISIT` and `ATPT` (a missing `ATPT` counts as one group of its own), flag the **last** record: the latest `ADT`, ties broken by the higher `AVAL` (a missing `AVAL` ranks lowest), then the higher `VSSEQ`. The flagged record gets `Y`.

Every other record, including every record that is not a candidate, gets a missing (null) `ANL01FL`.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.
