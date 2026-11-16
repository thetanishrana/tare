# ADOE: ABLFL (baseline flag for intraocular pressure, per eye)

`oe_upstream` holds ophthalmic measurements, one row per subject, parameter, eye and time point: `PARAMCD` is the parameter (all rows are intraocular pressure, `IOP`), `OELAT` the eye (`LEFT` or `RIGHT`), `OETPT` the time point (`PRE-DOSE` or `POST-DOSE`), `ADT` the date of the measurement, `AVAL` its value (sometimes missing) and `TRTSDT` the subject's first dose date.

Derive `ABLFL`, the baseline flag. For each subject, each `PARAMCD` and each **eye** separately, the baseline record is the **last** record that:

- has a non-missing `AVAL`,
- has `ADT` on or before `TRTSDT`, and
- has `OETPT` equal to `PRE-DOSE` (a post-dose measurement, even on the first dose day, is never baseline).

"Last" means the latest `ADT`; ties are broken by the higher `OESEQ`. `ABLFL` is `Y` on the baseline record and missing (null) on every other record, including all records of a subject, parameter and eye with no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `oe_upstream`, identified by `USUBJID` and `OESEQ`.
