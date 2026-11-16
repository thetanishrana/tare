# ADSL: STUDYEYE (study eye)

`sc_ophtha` holds subject characteristics for the ophthalmology study. The rows with `SCTESTCD` equal to `FOCID` give each subject's focus (study) eye in `SCSTRESC`: `OD` means the right eye and `OS` the left eye.

Derive `STUDYEYE`: `RIGHT` when `SCSTRESC` is `OD`, `LEFT` when it is `OS`, and missing (null) for a subject with no `FOCID` row or any other value.

Write one row for every subject in `dm`, including subjects who never received treatment.
