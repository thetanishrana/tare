# ADSL: EOSSTT (end-of-study status)

Derive `EOSSTT`, the end-of-study status, from the disposition records in `ds`: `COMPLETED` if the subject completed the study, `DISCONTINUED` if they left it early, and `ONGOING` otherwise.

Write one row for every subject in `dm`.
