# ADAE: AOCCIFL (first occurrence of the most severe event, within each body system)

Derive `AOCCIFL`, which marks one adverse event per subject and body system: the first occurrence of the most severe treatment-emergent event in that body system.

Look only at a subject's adverse events in `adae_upstream` with `TRTEMFL` equal to `Y`. Group them by subject and by `AEBODSYS` (a missing `AEBODSYS` counts as a group of its own). Within each group choose one event:

1. the most severe, by `ASEV` (`SEVERE` above `MODERATE` above `MILD`);
2. if several events share the highest severity, the one with the earliest `ASTDT`;
3. if several still tie, the one with the lowest `AESEQ`.

`AOCCIFL` is `Y` on each chosen event and missing (null) on every other event, including events that are not treatment-emergent.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
