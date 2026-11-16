# Spec ambiguity rating sheet

Each item below is a short specification for deriving one ADaM variable from SDTM-derived inputs. For each, imagine you are the programmer and answer:

1. **Ambiguous?** Would you need to ask a question before programming it? (yes / no)
2. **Open point:** if yes, what exactly is unclear? (one sentence)
3. **Confidence:** low / medium / high

Please rate from the text alone. Specs are fictional task text, not a real study.

## Item 1

# ADAE: AESTEFL (adverse event in the study eye)

`ae_upstream` holds one row per adverse event: `AELAT` is the eye the event affected (`LEFT`, `RIGHT` or `BOTH`; missing for events that are not eye events) and `STUDYEYE` the subject's study eye (`LEFT` or `RIGHT`).

Derive `AESTEFL`:

- missing (null) when `AELAT` is missing (the event is not an eye event);
- `Y` when `AELAT` is `BOTH`, or equals `STUDYEYE`;
- `N` when `AELAT` is the other eye (not the study eye).

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 2

# ADLB: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the lab results in `lb_upstream`: `Y` for results taken during treatment, that is between the subject's first dose date `TRTSDT` and last dose date `TRTEDT`; missing (null) otherwise. `ADT` is the result date and `AVISIT` the analysis visit name.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 3

# ADLB: ANRIND (reference range indicator)

Derive `ANRIND`, which says where each lab result lies against the normal range, for the results in `lb_upstream`. `AVAL` is the result, `ANRLO` the lower limit of the normal range and `ANRHI` the upper limit; either limit can be missing.

- `LOW` if `ANRLO` is present and `AVAL` is below it;
- `HIGH` if `ANRHI` is present and `AVAL` is above it;
- otherwise `NORMAL`. A result equal to a limit is `NORMAL`.

`ANRIND` is missing (null) when `AVAL` is missing, and when both `ANRLO` and `ANRHI` are missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 4

# ADLB: CHG (change from baseline)

Derive `CHG`, the change from baseline, for the lab results in `lb_upstream`. `AVAL` is the result, `BASE` the subject's baseline value for that parameter, and `AVISITN` the numeric analysis visit (0 is baseline).

`CHG` is `AVAL` minus `BASE` for **post-baseline** records only, meaning `AVISITN` is greater than 0. For every other record (baseline, earlier visits, or a missing `AVISITN`) `CHG` is missing (null). `CHG` is also missing if `AVAL` or `BASE` is missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 5

# ADLB: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the lab results in `lb_upstream`. `ADT` is the date of each result, `TRTSDT` the subject's first dose date, `TRTEDT` the last dose date and `AVISIT` the analysis visit name.

`ONTRTFL` is `Y` when all of these hold:

1. `ADT` is on or after `TRTSDT`;
2. `TRTEDT` is missing, or `ADT` is on or before `TRTEDT` (the last dose day is included; no window after it);
3. it is not a pre-dose measurement: a result whose `AVISIT` is `Baseline` and whose `ADT` is the first dose day (`ADT` equals `TRTSDT`) is taken before the first dose, so it is **not** on treatment.

In every case where the flag is not `Y`, `ONTRTFL` is missing (null).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 6

# ADLB: CHG (change from baseline)

Derive `CHG`, the change from baseline, for the lab results in `lb_upstream`: the result `AVAL` minus the subject's baseline value `BASE` for that parameter. `AVISITN` is the numeric analysis visit (0 is baseline).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 7

# ADOE: ABLFL (baseline flag for intraocular pressure)

`oe_upstream` holds ophthalmic measurements, one row per subject, parameter, eye and time point: `PARAMCD` is the parameter (all rows are intraocular pressure, `IOP`), `OELAT` the eye (`LEFT` or `RIGHT`), `OETPT` the time point (`PRE-DOSE` or `POST-DOSE`), `ADT` the date of the measurement, `AVAL` its value (sometimes missing) and `TRTSDT` the subject's first dose date.

Derive `ABLFL`, the baseline flag: `Y` on the baseline measurement, the last non-missing measurement before the first dose. Other records are missing (null).

Write one row per row of `oe_upstream`, identified by `USUBJID` and `OESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 8

# ADAE: AOCCIFL (first occurrence of the most severe event)

Derive `AOCCIFL`, which marks one adverse event per subject: the most severe treatment-emergent event (`TRTEMFL` is `Y` in `adae_upstream`). `Y` on that event, missing (null) on all others.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 9

# ADAE: AOCCIFL (first occurrence of the most severe event)

Derive `AOCCIFL`, which marks one adverse event per subject: the first occurrence of the most severe treatment-emergent event.

Look only at a subject's adverse events in `adae_upstream` with `TRTEMFL` equal to `Y`. Among them choose one event:

1. the most severe, by `ASEV` (`SEVERE` above `MODERATE` above `MILD`);
2. if several events share the highest severity, the one with the earliest `ASTDT`;
3. if several still tie, the one with the lowest `AESEQ`.

`AOCCIFL` is `Y` on the chosen event and missing (null) on every other event, including all events of a subject who has no treatment-emergent event.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 10

# ADLB: ANRIND (reference range indicator)

Derive `ANRIND`, which says where each lab result lies against the normal range, for the results in `lb_upstream`. `AVAL` is the result, `ANRLO` the lower limit of the normal range and `ANRHI` the upper limit. Results below the range are `LOW`, results above it are `HIGH`, and the rest are `NORMAL`.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 11

# ADVS: CHG (change from baseline)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (position and wait for blood pressure and pulse; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the analysis visit number `AVISITN` (0 is the baseline visit; screening and unscheduled records have none), the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `CHG`, the change from baseline: the result `AVAL` minus the subject's baseline value for the parameter, where the baseline is the last non-missing measurement on or before the first dose date.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 12

# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`, which holds the analysis start date `ASTDT` and the first and last dose dates `TRTSDT` and `TRTEDT`. An AE is treatment-emergent (`Y`) if it starts after the first dose and no more than 30 days after the last dose. Otherwise `TRTEMFL` is missing (null).

Write one row per row of `adae_upstream`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 13

# ADVS: CHG (change from baseline, per time point)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (position and wait for blood pressure and pulse; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the analysis visit number `AVISITN` (0 is the baseline visit; screening and unscheduled records have none), the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `CHG`, the change from baseline, in two steps.

1. **Baseline value, per time point.** For each subject, each `PARAMCD` and each value of `ATPT` (a missing `ATPT` is a group of its own), the baseline record is the last record with a non-missing `AVAL` and `ADT` on or before `TRTSDT` (latest `ADT`; ties by the higher `VISITNUM`, then the higher `VSSEQ`). Its `AVAL` is that time point's baseline value; time points are never compared with another time point's baseline.
2. **Change.** For **post-baseline** records only, meaning `AVISITN` greater than 0, `CHG` is `AVAL` minus the baseline value of the same subject, parameter and time point.

`CHG` is missing (null) on every other record (baseline, earlier or unscheduled visits, or a missing `AVISITN`), and whenever `AVAL` is missing or the time point has no baseline record.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 14

# ADSL: disposition dates (RANDDT, FRVDT, SCRFDT, EOSDT)

`ds` holds disposition and milestone records, one row per record, with the category `DSCAT`, the term `DSDECOD` and the start date `DSSTDTC` (a complete date). Derive four dates for every subject in `dm`: the randomization date `RANDDT`, the final retrieval visit date `FRVDT`, the screen failure date `SCRFDT` and the end-of-study date `EOSDT`, each taken from the matching disposition record. A date is missing when the subject has no such record.

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 15

# ADLB: SHIFT1 (shift from the baseline range category)

`lb_upstream` has one row per lab result: the subject `USUBJID`, the sequence number `LBSEQ`, the parameter `PARAMCD`, the baseline flag `ABLFL` (`Y` on each subject-parameter's baseline record, otherwise missing) and the reference range indicator `ANRIND` (`LOW`, `NORMAL`, `HIGH`, or missing).

Derive `SHIFT1`, the text `<baseline category> to <category of this record>`, on every row:

- the baseline category `BNRIND` is the `ANRIND` of the subject's baseline record (`ABLFL` equal to `Y`) for the same `PARAMCD`; it is `NULL` (the word) when the subject has no baseline record for that parameter, or the baseline record's `ANRIND` is missing;
- the category of this record is its own `ANRIND`, or `NULL` (the word) when missing.

For example `NORMAL to HIGH`, `LOW to LOW`, `NULL to NORMAL`. `SHIFT1` is never missing.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 16

# ADSL: TRTSDT (treatment start date)

Derive `TRTSDT`, the date each subject started study treatment.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

Only records whose start date `EXSTDTC` is a complete date (year, month and day all present) can be used; a record with a partial or missing start date is ignored.

`TRTSDT` is the earliest `EXSTDTC` date among the subject's usable qualifying records. A subject with no usable qualifying record gets a missing `TRTSDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 17

# ADAE: AENDT and AENDTF (analysis end date and imputation flag)

Derive `AENDT`, the analysis end date of each adverse event in `ae`, from the (possibly partial) ISO 8601 end date `AEENDTC`, and `AENDTF`, the flag saying which part was imputed. `adsl_upstream` gives each subject's death date `DTHDT` and study completion date `EOSDT` as dates (either can be missing).

| `AEENDTC` | `AENDT` | `AENDTF` |
|---|---|---|
| complete date | that date | missing (null) |
| year and month only | the **last** day of that month | `D` |
| year only | 31 December of that year | `M` |
| missing or empty | missing (null) | missing (null) |

Ignore any time of day.

**Cap for imputed dates.** Take the earliest of the subject's `DTHDT` and `EOSDT` that are present. If a date was imputed, that earliest date is earlier than the imputed date and it falls inside the period the partial date covers (it is on or after the first day of that month for a year-month date, or of that year for a year-only date), then `AENDT` is that earliest date instead. If the earliest date lies before the period, nothing is adjusted. `AENDTF` is unchanged. Complete dates are never adjusted, and nothing is adjusted when both `DTHDT` and `EOSDT` are missing.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 18

# ADSL: LSTALVDT (last known alive date)

Derive `LSTALVDT`, the last date the subject is known to have been alive, as the latest date on which the subject has a dated record in the study data. The datasets provided are `ae`, `lb`, `vs` and `adsl_upstream` (which holds the treatment end date `TRTEDT`). Missing if there is no usable date.

Write one row for every subject in `dm`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 19

# ADSL: EOSSTT (end-of-study status)

Derive `EOSSTT`, the end-of-study status, from the disposition records in `ds`.

Use only rows of `ds` where `DSCAT` is `DISPOSITION EVENT`. A subject has at most one such row. Look at its `DSDECOD`:

| Situation | `EOSSTT` |
|---|---|
| `DSDECOD` is `COMPLETED` | `COMPLETED` |
| `DSDECOD` is `SCREEN FAILURE` | missing (null): screen failures have no study status |
| any other `DSDECOD` | `DISCONTINUED` |
| the subject has no such row | `ONGOING` |

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 20

# ADSL: TRTSDT (treatment start date)

Derive `TRTSDT`, the date each subject started study treatment: the date of their first exposure record in `ex`, using the start date `EXSTDTC`. Missing if the subject has no usable exposure record.

Write one row for every subject in `dm`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 21

# ADAE: AENDT and AENDTF (analysis end date and imputation flag)

Derive `AENDT`, the analysis end date of each adverse event in `ae`, from the (possibly partial) ISO 8601 end date `AEENDTC`, and `AENDTF`, the imputation flag: `D` when the day was imputed, `M` when the month and day were imputed, missing when nothing was imputed. Fill in the missing parts of a partial date; a missing end date stays missing. `adsl_upstream` gives each subject's death date `DTHDT` and study completion date `EOSDT` as dates (either can be missing). Ignore any time of day.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 22

# ADVS: ABLFL (baseline flag, separately for each time point)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (for blood pressure and pulse the position and wait, for example `AFTER LYING DOWN FOR 5 MINUTES`; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `ABLFL`, the baseline flag. Baseline is chosen **separately for each time point**: for each subject, each `PARAMCD` and each value of `ATPT` (a missing `ATPT` counts as one group of its own), the baseline record is the **last** record that has a non-missing `AVAL` and `ADT` on or before `TRTSDT`. "Last" means the latest `ADT`; ties are broken by the higher `VISITNUM`, then the higher `VSSEQ`.

`ABLFL` is `Y` on the baseline record and missing (null) on every other record, including all records of a group with no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 23

# ADAE: AESTEFL (adverse event in the study eye)

`ae_upstream` holds one row per adverse event: `AELAT` is the eye the event affected (`LEFT`, `RIGHT` or `BOTH`; missing for events that are not eye events) and `STUDYEYE` the subject's study eye (`LEFT` or `RIGHT`).

Derive `AESTEFL`, which marks the adverse events that occurred in the study eye.

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 24

# ADAE: ADURN (adverse event duration in days)

Derive `ADURN`, how long each adverse event lasted in days, from the start date `ASTDT` and end date `AENDT` in `adae_upstream`. Missing if the duration cannot be determined.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 25

# ADLB: PCHG (percent change from baseline)

Derive `PCHG`, the percent change from baseline, for the lab results in `lb_upstream`. `AVAL` is the result, `BASE` the subject's baseline value for that parameter and `AVISITN` the numeric analysis visit (0 is baseline).

For **post-baseline** records only (`AVISITN` greater than 0), `PCHG` is `100 * (AVAL - BASE) / BASE`.

`PCHG` is missing (null) for every other record (baseline, earlier visits), when `AVAL` or `BASE` is missing, and when `BASE` is 0 (no percentage can be formed). Do not round.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 26

# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` and the subject's first dose date `TRTSDT`. It counts days relative to the first dose. Missing if either date is missing.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 27

# ADVS: summary records (the average of repeated readings)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the parameter `PARAMCD`, the measurement date `ADT`, the analysis visit `AVISIT` (the text `(none)` when the measurement belongs to no analysis visit), the time point `ATPT` and the result `AVAL` (a few results are missing).

Derive the summary records: for each subject, parameter and visit, one row holding the average of the readings taken then.

Write one row per summary record, with the columns `USUBJID`, `PARAMCD`, `ADT`, `AVISIT` and `AVAL`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 28

# ADVS: summary records (the average of repeated readings)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the parameter `PARAMCD`, the measurement date `ADT`, the analysis visit `AVISIT` (the text `(none)` when the measurement belongs to no analysis visit, for example screening or unscheduled measurements), the time point `ATPT` and the result `AVAL` (a few results are missing).

Derive the summary records. For every distinct combination of `USUBJID`, `PARAMCD`, `ADT` and `AVISIT`, write one row whose `AVAL` is the arithmetic mean of the non-missing `AVAL` values in that combination. Do not round. A combination that has a single non-missing result still gets a row (its mean is that result). A combination with no non-missing result gets no row.

Write one row per combination, with the columns `USUBJID`, `PARAMCD`, `ADT`, `AVISIT` and `AVAL`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 29

# ADAE: ASTDT and ASTDTF (analysis start date and imputation flag)

Derive `ASTDT`, the analysis start date of each adverse event in `ae`, from the (possibly partial) ISO 8601 start date `AESTDTC`, and `ASTDTF`, the flag saying which part was imputed.

| `AESTDTC` | `ASTDT` | `ASTDTF` |
|---|---|---|
| complete date | that date | missing (null) |
| year and month only | the first day of that month | `D` |
| year only | 1 January of that year | `M` |
| missing or empty | missing (null) | missing (null) |

Ignore any time of day.

**First-dose adjustment.** `adsl_upstream` gives each subject's first dose date `TRTSDT`. If a date was imputed, the imputed date is earlier than `TRTSDT`, and `TRTSDT` lies inside the period the partial date covers (the same month for a year-month date, the same year for a year-only date), then `ASTDT` is `TRTSDT` instead: the event may have started on the first dose day. `ASTDTF` is unchanged. Complete dates are never adjusted, and nothing is adjusted when `TRTSDT` is missing.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 30

# ADVS: ABLFL (baseline flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (for blood pressure and pulse the position and wait, for example `AFTER LYING DOWN FOR 5 MINUTES`; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `ABLFL`, the baseline flag: `Y` on the baseline measurement, the last non-missing measurement of each parameter before the first dose. Other records are missing (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 31

# ADSL: SAFFL (safety population flag)

Derive `SAFFL`, the safety population flag.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

`SAFFL` is `Y` for a subject with at least one qualifying exposure record, and `N` otherwise. It is never missing.

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 32

# ADAE: LDOSEDTM and DOSEON (last dose before an event, and the dose in effect)

For each adverse event in `ae_upstream` (which gives its start date `ASTDT`), derive `LDOSEDTM`, the date of the last dose on or before the event start, and `DOSEON`, the dose in effect on the event start date. Use the exposure records in `ex`.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or `EXDOSE` equals 0 and `EXTRT` contains `PLACEBO`, and whose start date `EXSTDTC` is a complete date. Ignore all other rows. All dosing is once daily.

**`LDOSEDTM`.** A qualifying record that also has a complete end date `EXENDTC` represents one dose on every calendar day from its start date to its end date, both included. `LDOSEDTM` is the latest such dosing day that is on or before `ASTDT`, written as a date (time of day is not collected). Records without a complete end date are not used for `LDOSEDTM`. If there is no such day, `LDOSEDTM` is missing (null).

**`DOSEON`.** Among the subject's qualifying records that have started on or before `ASTDT` and that either end on or after `ASTDT` or have no end date at all (still open), take the one with the latest start date. `DOSEON` is its `EXDOSE`. If there is no such record, `DOSEON` is missing (null).

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 33

# ADSL: LSTALVDT (last known alive date)

Derive `LSTALVDT`, the last date the subject is known to have been alive: the **latest** of these dates for the subject.

- AE start dates (`AESTDTC` in `ae`)
- AE end dates (`AEENDTC` in `ae`)
- lab sample dates (`LBDTC` in `lb`)
- the treatment end date `TRTEDT` (from `adsl_upstream`, already a date)

Dates in `ae`, `lb` are ISO 8601 text. Convert each to a calendar date as follows: ignore any time of day; if only the year and month are present use the first day of that month; if only the year is present use 1 January of that year; skip empty or missing values.

A subject with no usable date from any source gets a missing `LSTALVDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 34

# ADLB: ABLFL (baseline record flag)

Derive `ABLFL` for the lab results in `lb_upstream`: for each subject and parameter (`PARAMCD`), flag with `Y` the baseline record, which is the last non-missing result before the subject's first dose date `TRTSDT`. Other records are missing (null).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 35

# ADSL: disposition dates (RANDDT, FRVDT, SCRFDT, EOSDT)

`ds` holds disposition and milestone records, one row per record, with the category `DSCAT`, the term `DSDECOD` and the start date `DSSTDTC` (a complete date). Derive four dates for every subject in `dm`:

- `RANDDT`, the randomization date: `DSSTDTC` of the subject's record whose `DSDECOD` is `RANDOMIZED`.
- `FRVDT`, the final retrieval visit date: `DSSTDTC` of the record whose `DSDECOD` is `FINAL RETRIEVAL VISIT`.
- `SCRFDT`, the screen failure date: `DSSTDTC` of the record whose `DSCAT` is `DISPOSITION EVENT` and whose `DSDECOD` is `SCREEN FAILURE`.
- `EOSDT`, the end-of-study date: `DSSTDTC` of the record whose `DSCAT` is `DISPOSITION EVENT`, **except** that a screen failure has no end-of-study date (their disposition date is `SCRFDT`).

A date is missing (null) when the subject has no such record. A subject has at most one record of each kind.

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 36

# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` and the subject's first dose date `TRTSDT`.

Study days have no day 0. The first dose day is study day 1, the day before it is study day -1, and so on:

- if `ASTDT` is on or after `TRTSDT`: `ASTDY` is `ASTDT` minus `TRTSDT` in days, plus 1;
- if `ASTDT` is before `TRTSDT`: `ASTDY` is `ASTDT` minus `TRTSDT` in days (a negative number).

If either date is missing, `ASTDY` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 37

# ADOE: ABLFL (baseline flag for intraocular pressure, per eye)

`oe_upstream` holds ophthalmic measurements, one row per subject, parameter, eye and time point: `PARAMCD` is the parameter (all rows are intraocular pressure, `IOP`), `OELAT` the eye (`LEFT` or `RIGHT`), `OETPT` the time point (`PRE-DOSE` or `POST-DOSE`), `ADT` the date of the measurement, `AVAL` its value (sometimes missing) and `TRTSDT` the subject's first dose date.

Derive `ABLFL`, the baseline flag. For each subject, each `PARAMCD` and each **eye** separately, the baseline record is the **last** record that:

- has a non-missing `AVAL`,
- has `ADT` on or before `TRTSDT`, and
- has `OETPT` equal to `PRE-DOSE` (a post-dose measurement, even on the first dose day, is never baseline).

"Last" means the latest `ADT`; ties are broken by the higher `OESEQ`. `ABLFL` is `Y` on the baseline record and missing (null) on every other record, including all records of a subject, parameter and eye with no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `oe_upstream`, identified by `USUBJID` and `OESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 38

# ADAE: ADURN (adverse event duration in days)

Derive `ADURN`, the duration of each adverse event in days, from the start date `ASTDT` and end date `AENDT` in `adae_upstream`.

The duration counts both the first and the last day: `AENDT` minus `ASTDT` in days, plus 1. An event that starts and ends on the same day lasts 1 day.

If `AENDT` or `ASTDT` is missing (for instance an event that is still ongoing), `ADURN` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 39

# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`. It already holds the analysis start date `ASTDT`, the first dose date `TRTSDT` and the last dose date `TRTEDT` as dates. (The AE end date `AENDT` is present but is not used.)

An AE is treatment-emergent (`TRTEMFL` = `Y`) when both hold:

1. it started on or after the first dose date: `ASTDT` is on or after `TRTSDT`; and
2. it started no later than **30 days after** the last dose date: `ASTDT` is on or before `TRTEDT` plus 30 days (the 30th day is included). If `TRTEDT` is missing there is no upper limit.

If `ASTDT` or `TRTSDT` is missing, the flag is not set. In every case where the flag is not `Y`, `TRTEMFL` is missing (null), not `N`.

Write one row per row of `adae_upstream`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 40

# ADAE: ASTDT and ASTDTF (analysis start date and imputation flag)

Derive `ASTDT`, the analysis start date of each adverse event in `ae`, from the (possibly partial) ISO 8601 start date `AESTDTC`, and `ASTDTF`, the imputation flag: `D` when the day was imputed, `M` when the month was imputed (and the day), and missing when nothing was imputed. Impute missing parts to the earliest possible date, but do not put an imputed start before the subject's first dose date `TRTSDT` (from `adsl_upstream`) when the event could have started on or after it. Ignore time of day.

Write one row per row of `ae`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 41

# ADSL: SAFFL (safety population flag)

Derive `SAFFL`, the safety population flag: `Y` for every subject who received study treatment (according to the exposure records in `ex`), `N` otherwise.

Write one row for every subject in `dm`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 42

# ADAE: LDOSEDTM and DOSEON (last dose before an event, and the dose in effect)

For each adverse event in `ae_upstream` (which gives its start date `ASTDT`), derive `LDOSEDTM`, the date of the last dose on or before the event start, and `DOSEON`, the dose in effect on the event start date. Use the exposure records in `ex`, where an exposure record covers a period from its start date `EXSTDTC` to its end date `EXENDTC`. Ignore records that did not give study treatment.

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 43

# ADLB: PCHG (percent change from baseline)

Derive `PCHG`, the percent change from baseline, for the lab results in `lb_upstream`: the change of the result `AVAL` from the subject's baseline value `BASE`, expressed as a percentage of the baseline. `AVISITN` is the numeric analysis visit (0 is baseline).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 44

# ADLB: SHIFT1 (shift from the baseline range category)

`lb_upstream` has one row per lab result: the subject `USUBJID`, the sequence number `LBSEQ`, the parameter `PARAMCD`, the baseline flag `ABLFL` (`Y` on each subject-parameter's baseline record, otherwise missing) and the reference range indicator `ANRIND` (`LOW`, `NORMAL`, `HIGH`, or missing).

Derive `SHIFT1`, describing how the reference range category of each result has shifted from the subject's baseline category for the same parameter, written like `NORMAL to HIGH`.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 45

# ADSL: EOSSTT (end-of-study status)

Derive `EOSSTT`, the end-of-study status, from the disposition records in `ds`: `COMPLETED` if the subject completed the study, `DISCONTINUED` if they left it early, and `ONGOING` otherwise.

Write one row for every subject in `dm`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 46

# ADSL: TRTDURD (treatment duration)

Derive `TRTDURD`, the number of days each subject was on treatment, from the treatment start date `TRTSDT` and end date `TRTEDT` in `adsl_upstream`. It is missing if either date is missing.

Write one row per row of `adsl_upstream` (one per subject).

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 47

# ADLB: ABLFL (baseline record flag)

Derive `ABLFL`, the baseline record flag, for the lab results in `lb_upstream`. `ADT` is the analysis date of each result and `TRTSDT` the subject's first dose date.

For each subject and each `PARAMCD`, the baseline record is the **last** record that:

- has a non-missing `AVAL`, and
- has `ADT` on or before `TRTSDT` (a result on the first dose day counts).

"Last" means latest `ADT`; ties on `ADT` are broken by higher `VISITNUM`, and then by higher `LBSEQ`.

`ABLFL` is `Y` on the baseline record. It is missing (null) on every other record, including all records of a subject and parameter that has no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 48

# ADSL: TRTDURD (treatment duration in days)

Derive `TRTDURD`, the treatment duration in days, from the treatment start date `TRTSDT` and end date `TRTEDT` in `adsl_upstream`.

`TRTDURD` counts both the first and the last day of treatment: `TRTEDT` minus `TRTSDT` in days, plus 1. A subject whose start and end fall on the same day has a duration of 1.

If either date is missing, `TRTDURD` is missing.

Write one row per row of `adsl_upstream` (one per subject).

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

