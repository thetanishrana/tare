# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`. It holds the analysis start date `ASTDT` (a start date given only as a month or year has already been filled in to a full date, and `ASTDTF` says so: `D` when the day was filled in, `M` when the month and day were; `ASTDT` is missing when the event has no start date at all), the AE end date `AENDT` (missing when unknown or ongoing), the first dose date `TRTSDT` and the last dose date `TRTEDT`.

An AE is treatment-emergent (`TRTEMFL` = `Y`) in either of these cases:

1. `ASTDT` is present, it is on or after `TRTSDT`, and it is no later than **30 days after** the last dose date (`ASTDT` on or before `TRTEDT` plus 30 days, the 30th day included; if `TRTEDT` is missing there is no upper limit). A filled-in `ASTDT` is used exactly like a complete one.
2. `ASTDT` is missing, and either `AENDT` is missing or `AENDT` is on or after `TRTSDT` (an event with no start date is assumed to have started during treatment unless it is known to have ended before the first dose).

If `TRTSDT` is missing the flag is not set. In every case where the flag is not `Y`, `TRTEMFL` is missing (null), not `N`.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.
