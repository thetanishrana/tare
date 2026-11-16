# ADAE: AOCCIFL (first occurrence of the most severe event)

Derive `AOCCIFL`, which marks one adverse event per subject: the most severe treatment-emergent event (`TRTEMFL` is `Y` in `adae_upstream`). `Y` on that event, missing (null) on all others.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
