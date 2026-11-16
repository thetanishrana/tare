# ADOE: ABLFL (baseline flag for intraocular pressure)

`oe_upstream` holds ophthalmic measurements, one row per subject, parameter, eye and time point: `PARAMCD` is the parameter (all rows are intraocular pressure, `IOP`), `OELAT` the eye (`LEFT` or `RIGHT`), `OETPT` the time point (`PRE-DOSE` or `POST-DOSE`), `ADT` the date of the measurement, `AVAL` its value (sometimes missing) and `TRTSDT` the subject's first dose date.

Derive `ABLFL`, the baseline flag: `Y` on the baseline measurement, the last non-missing measurement before the first dose. Other records are missing (null).

Write one row per row of `oe_upstream`, identified by `USUBJID` and `OESEQ`.
