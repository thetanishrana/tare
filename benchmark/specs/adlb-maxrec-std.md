# ADLB: MAXIMUM records (derived post-baseline maximum)

Create one derived record per subject and parameter that holds the subject's **maximum on-treatment value**, from the lab results in `lb_upstream`.

Consider only records with a non-missing `AVAL` and `ONTRTFL` equal to `Y`. For each subject and each `PARAMCD`, choose one of these records:

1. the one with the highest `AVAL`;
2. if several share the highest value, the one with the earliest `ADT`;
3. if several still tie, the one with the lowest `AVISITN`.

Write one output row per subject and `PARAMCD` that has at least one qualifying record (and no row for a subject and parameter without one). Copy `LBSEQ`, `AVAL` and `ADT` from the chosen record. The output is identified by `USUBJID` and `PARAMCD`.
