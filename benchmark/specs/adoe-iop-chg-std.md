# ADOE: CHG (change from baseline in intraocular pressure, per eye)

`oe_upstream` holds ophthalmic measurements, one row per subject, parameter, eye and time point: `PARAMCD` is the parameter (all rows are intraocular pressure, `IOP`), `OELAT` the eye (`LEFT` or `RIGHT`), `OETPT` the time point (`PRE-DOSE` or `POST-DOSE`), `ADT` the date of the measurement, `AVAL` its value (sometimes missing) and `TRTSDT` the subject's first dose date.

Derive `CHG`, the change from baseline, in two steps.

1. **Baseline value, per eye.** For each subject, each `PARAMCD` and each eye separately, the baseline record is the last record with a non-missing `AVAL`, `ADT` on or before `TRTSDT` and `OETPT` equal to `PRE-DOSE` (latest `ADT`; ties by the higher `OESEQ`). Its `AVAL` is that eye's baseline value. The two eyes of a subject have their own baselines; an eye's records are never compared with the other eye's baseline.
2. **Change.** For **post-baseline** records only, meaning `ADT` strictly after `TRTSDT`, `CHG` is `AVAL` minus that eye's baseline value.

`CHG` is missing (null) on every other record (on or before the first dose date, or with a missing `ADT` or `TRTSDT`), and whenever `AVAL` is missing or the eye has no baseline record.

Write one row per row of `oe_upstream`, identified by `USUBJID` and `OESEQ`.
