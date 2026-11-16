# ADAE: AOCCIFL (first occurrence of the most severe event)

Derive `AOCCIFL`, which marks one adverse event per subject: the first occurrence of the most severe treatment-emergent event.

Look only at a subject's adverse events in `adae_upstream` with `TRTEMFL` equal to `Y`. Among them choose one event:

1. the most severe, by `ASEV` (`SEVERE` above `MODERATE` above `MILD`);
2. if several events share the highest severity, the one with the earliest `ASTDT` (an event with a missing `ASTDT` ranks after every event that has one);
3. if several still tie, the one with the lowest `AESEQ`.

`AOCCIFL` is `Y` on the chosen event and missing (null) on every other event, including all events of a subject who has no treatment-emergent event.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
