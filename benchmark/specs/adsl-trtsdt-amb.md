# ADSL: TRTSDT (treatment start date)

Derive `TRTSDT`, the date each subject started study treatment: the date of their first exposure record in `ex`, using the start date `EXSTDTC`. Missing if the subject has no usable exposure record.

Write one row for every subject in `dm`.
