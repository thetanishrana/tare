# Spec ambiguity rating sheet

Each item below is a short specification for deriving one ADaM variable from SDTM-derived inputs. For each, imagine you are the programmer and answer:

1. **Ambiguous?** Would you need to ask a question before programming it? (yes / no)
2. **Open point:** if yes, what exactly is unclear? (one sentence)
3. **Confidence:** low / medium / high

Please rate from the text alone. Specs are fictional task text, not a real study.

## Item 1

# ADVS: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the vital-sign measurements in `advs_upstream`: `Y` for measurements taken during treatment, that is between the subject's first dose date `TRTSDT` and last dose date `TRTEDT`; missing (null) otherwise. `ADT` is the measurement date and `AVISIT` the analysis visit name.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 2

# ADVS: ADY (analysis study day)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the measurement date `ADT` and the subject's first dose date `TRTSDT`.

Derive `ADY`, the study day of the measurement relative to the first dose, using the usual clinical-trial convention in which there is no day 0: the first dose day is day 1 and the day before it is day -1. For a measurement on or after the first dose date `ADY` is the number of calendar days from `TRTSDT` to `ADT` plus 1; for a measurement before the first dose date it is the plain difference (a negative number).

`ADY` is missing (null) when `ADT` or `TRTSDT` is missing.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 3

# ADLB: ABLFL (baseline record flag)

Derive `ABLFL` for the lab results in `lb_upstream`: for each subject and parameter (`PARAMCD`), flag with `Y` the baseline record, which is the last non-missing result before the subject's first dose date `TRTSDT`. Other records are missing (null).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 4

# ADVS: ANL01FL (analysis record flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (missing for parameters measured once per visit), the analysis visit name `AVISIT` and number `AVISITN` (both missing for measurements that fall outside the scheduled visits), the measurement date `ADT`, the result `AVAL` (a few are missing) and the on-treatment flag `ONTRTFL` (`Y` or missing).

Derive `ANL01FL`, the analysis record flag: `Y` on the record used for analysis, the last measurement of each subject, parameter and analysis visit; missing (null) on all other records.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 5

# ADVS: ADY (analysis study day)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the measurement date `ADT` and the subject's first dose date `TRTSDT`.

Derive `ADY`, the study day of the measurement relative to the first dose date. `ADY` is missing (null) when `ADT` or `TRTSDT` is missing.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 6

# ADVS: AVISIT (analysis visit)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the visit name as collected `VISIT` (capital letters, for example `BASELINE` or `WEEK 12`) and the visit number `VISITNUM`.

Derive `AVISIT`, the analysis visit name:

- a `VISIT` containing any of the texts `SCREEN`, `UNSCHED`, `RETRIEVAL` or `AMBUL` is not an analysis visit: `AVISIT` is missing (null);
- every other `VISIT` becomes its text in title case (first letter of each word capital, the rest lower case), so `BASELINE` gives `Baseline` and `WEEK 12` gives `Week 12`.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 7

# ADSL: TRTEDT (treatment end date)

Derive `TRTEDT`, the date each subject received their last study treatment.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or where `EXDOSE` equals 0 and `EXTRT` contains the text `PLACEBO` (placebo rows legitimately have a dose of 0). Rows with a missing `EXDOSE` do not qualify.

Only records whose end date `EXENDTC` is a complete date (year, month and day all present) can be used; a record with a partial or missing end date is ignored (the start date is not used as a substitute).

`TRTEDT` is the latest `EXENDTC` date among the subject's usable qualifying records. A subject with no usable qualifying record gets a missing `TRTEDT`.

Write one row for every subject in `dm`, including subjects who never received treatment.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 8

# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` (a start date given only as a month or year has been filled in to a full date, and `ASTDTF` says so; `ASTDT` is missing when the event has no start date) and the subject's first dose date `TRTSDT`. It counts days relative to the first dose. Missing if the start date or the first dose date is missing.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 9

# ADAE: AOCCIFL (first occurrence of the most severe event)

Derive `AOCCIFL`, which marks one adverse event per subject: the most severe treatment-emergent event (`TRTEMFL` is `Y` in `adae_upstream`). `Y` on that event, missing (null) on all others.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 10

# ADVS: CHG (change from baseline)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (position and wait for blood pressure and pulse; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the analysis visit number `AVISITN` (0 is the baseline visit; screening and unscheduled records have none), the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `CHG`, the change from baseline: the result `AVAL` minus the subject's baseline value for the parameter, where the baseline is the last non-missing measurement on or before the first dose date.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 11

# ADAE: LDOSEDTM and DOSEON (last dose before an event, and the dose in effect)

For each adverse event in `ae_upstream` (which gives its start date `ASTDT`), derive `LDOSEDTM`, the date of the last dose on or before the event start, and `DOSEON`, the dose in effect on the event start date. Use the exposure records in `ex`, where an exposure record covers a period from its start date `EXSTDTC` to its end date `EXENDTC`. Ignore records that did not give study treatment.

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 12

# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`, which holds the analysis start date `ASTDT` (a start date given only as a month or year has been filled in to a full date, and `ASTDTF` says so; `ASTDT` is missing when the event has no start date), the AE end date `AENDT`, and the first and last dose dates `TRTSDT` and `TRTEDT`. An AE is treatment-emergent (`Y`) if it starts after the first dose and no more than 30 days after the last dose. Otherwise `TRTEMFL` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 13

# ADVS: AVISIT (analysis visit)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the visit name as collected `VISIT` (capital letters, for example `BASELINE` or `WEEK 12`) and the visit number `VISITNUM`.

Derive `AVISIT`, the analysis visit name, in the style `Baseline`, `Week 2`, `Week 4`. Visits that are not analysis visits get no analysis visit name (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 14

# ADVS: ABLFL (baseline flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (for blood pressure and pulse the position and wait, for example `AFTER LYING DOWN FOR 5 MINUTES`; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `ABLFL`, the baseline flag: `Y` on the baseline measurement, the last non-missing measurement of each parameter before the first dose. Other records are missing (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 15

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

## Item 16

# ADVS: ABLFL (baseline flag, separately for each time point)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (for blood pressure and pulse the position and wait, for example `AFTER LYING DOWN FOR 5 MINUTES`; missing for parameters measured once per visit), the visit number `VISITNUM`, the measurement date `ADT`, the result `AVAL` (a few are missing) and the subject's first dose date `TRTSDT`.

Derive `ABLFL`, the baseline flag. Baseline is chosen **separately for each time point**: for each subject, each `PARAMCD` and each value of `ATPT` (a missing `ATPT` counts as one group of its own), the baseline record is the **last** record that has a non-missing `AVAL` and `ADT` on or before `TRTSDT`. "Last" means the latest `ADT`; ties are broken by the higher `VISITNUM`, then the higher `VSSEQ`.

`ABLFL` is `Y` on the baseline record and missing (null) on every other record, including all records of a group with no qualifying record. A record with a missing `ADT` or `TRTSDT` cannot be baseline.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 17

# ADAE: TRTEMFL (treatment-emergent flag)

Derive `TRTEMFL`, the treatment-emergent flag, for each adverse event in `adae_upstream`. It holds the analysis start date `ASTDT` (a start date given only as a month or year has already been filled in to a full date, and `ASTDTF` says so: `D` when the day was filled in, `M` when the month and day were; `ASTDT` is missing when the event has no start date at all), the AE end date `AENDT` (missing when unknown or ongoing), the first dose date `TRTSDT` and the last dose date `TRTEDT`.

An AE is treatment-emergent (`TRTEMFL` = `Y`) in either of these cases:

1. `ASTDT` is present, it is on or after `TRTSDT`, and it is no later than **30 days after** the last dose date (`ASTDT` on or before `TRTEDT` plus 30 days, the 30th day included; if `TRTEDT` is missing there is no upper limit). A filled-in `ASTDT` is used exactly like a complete one.
2. `ASTDT` is missing, and either `AENDT` is missing or `AENDT` is on or after `TRTSDT` (an event with no start date is assumed to have started during treatment unless it is known to have ended before the first dose).

If `TRTSDT` is missing the flag is not set. In every case where the flag is not `Y`, `TRTEMFL` is missing (null), not `N`.

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 18

# ADVS: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the vital-sign measurements in `advs_upstream`: `Y` for measurements taken during treatment, that is between the subject's first dose date `TRTSDT` and last dose date `TRTEDT`; missing (null) otherwise. `ADT` is the measurement date and `AVISIT` the analysis visit name.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 19

# ADLB: R2BASE (ratio to baseline)

`lb_upstream` has one row per laboratory result: the subject `USUBJID`, the sequence number `LBSEQ` (unique within a subject), the parameter `PARAMCD`, the analysis visit number `AVISITN`, the result `AVAL` (some are missing) and the subject's baseline value for that parameter `BASE` (missing when the subject has no baseline).

Derive `R2BASE`, the ratio of the result to the baseline: `AVAL` divided by `BASE`, as a plain ratio (1.0 means no change; it is not a percentage and is not rounded). It is derived for every record, baseline and pre-baseline records included.

`R2BASE` is missing (null) when `AVAL` is missing, when `BASE` is missing, or when `BASE` is 0 (a ratio to a zero baseline is not defined, including 0 divided by 0).

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 20

# ADVS: ANL01FL (analysis record flag)

`advs_upstream` has one row per vital-sign measurement: the subject `USUBJID`, the sequence number `VSSEQ` (unique within a subject), the parameter `PARAMCD`, the time point `ATPT` (missing for parameters measured once per visit), the analysis visit name `AVISIT` and number `AVISITN` (both missing for measurements that fall outside the scheduled visits), the measurement date `ADT`, the result `AVAL` (a few are missing) and the on-treatment flag `ONTRTFL` (`Y` or missing).

Derive `ANL01FL`, the analysis record flag. Only records with `ONTRTFL` equal to `Y` **and** a non-missing `AVISITN` are candidates. Among the candidates, for each subject, `PARAMCD`, `AVISIT` and `ATPT` (a missing `ATPT` counts as one group of its own), flag the **last** record: the latest `ADT`, ties broken by the higher `AVAL` (a missing `AVAL` ranks lowest), then the higher `VSSEQ`. The flagged record gets `Y`.

Every other record, including every record that is not a candidate, gets a missing (null) `ANL01FL`.

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 21

# ADVS: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the vital-sign measurements in `advs_upstream`. `ADT` is the measurement date, `TRTSDT` the subject's first dose date, `TRTEDT` the last dose date and `AVISIT` the analysis visit name.

`ONTRTFL` is `Y` when all of these hold:

1. `ADT` is on or after `TRTSDT`;
2. `TRTEDT` is missing, or `ADT` is on or before `TRTEDT` (the last dose day is included; there is no window after it);
3. it is not a pre-dose measurement: a measurement whose `AVISIT` is `Baseline` and whose `ADT` is the first dose day (`ADT` equals `TRTSDT`) is taken before the first dose, so it is **not** on treatment.

A measurement of a subject whose first dose date `TRTSDT` is missing cannot be on treatment.

In every case where the flag is not `Y`, `ONTRTFL` is missing (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 22

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

## Item 23

# ADAE: ASTDY (analysis start study day)

Derive `ASTDY`, the study day on which each adverse event started, in `adae_upstream`, which holds the event start date `ASTDT` (a start date given only as a month or year has already been filled in to a full date, and `ASTDTF` says so: `D` or `M`; `ASTDT` is missing when the event has no start date) and the subject's first dose date `TRTSDT`.

Study days have no day 0. The first dose day is study day 1, the day before it is study day -1, and so on:

- if `ASTDT` is on or after `TRTSDT`: `ASTDY` is `ASTDT` minus `TRTSDT` in days, plus 1;
- if `ASTDT` is before `TRTSDT`: `ASTDY` is `ASTDT` minus `TRTSDT` in days (a negative number).

A filled-in `ASTDT` is used exactly like a complete one, whatever `ASTDTF` says. If `ASTDT` or `TRTSDT` is missing, `ASTDY` is missing (null).

Write one row per row of `adae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 24

# ADLB: R2BASE (ratio to baseline)

`lb_upstream` has one row per laboratory result: the subject `USUBJID`, the sequence number `LBSEQ` (unique within a subject), the parameter `PARAMCD`, the analysis visit number `AVISITN`, the result `AVAL` (some are missing) and the subject's baseline value for that parameter `BASE` (missing when the subject has no baseline).

Derive `R2BASE`, each result expressed relative to the subject's baseline value for the parameter: `AVAL` compared with `BASE`.

Write one row per row of `lb_upstream`, identified by `USUBJID` and `LBSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 25

# ADAE: LDOSEDTM and DOSEON (last dose before an event, and the dose in effect)

For each adverse event in `ae_upstream` (which gives its start date `ASTDT`), derive `LDOSEDTM`, the date of the last dose on or before the event start, and `DOSEON`, the dose in effect on the event start date. Use the exposure records in `ex`.

A **qualifying exposure record** is a row of `ex` where `EXDOSE` is above 0, or `EXDOSE` equals 0 and `EXTRT` contains `PLACEBO`, and whose start date `EXSTDTC` is a complete date. Ignore all other rows. All dosing is once daily.

**`LDOSEDTM`.** A qualifying record that also has a complete end date `EXENDTC` represents one dose on every calendar day from its start date to its end date, both included. `LDOSEDTM` is the latest such dosing day that is on or before `ASTDT`, written as a date (time of day is not collected). Records without a complete end date are not used for `LDOSEDTM`. If there is no such day, `LDOSEDTM` is missing (null).

**`DOSEON`.** Among the subject's qualifying records that have started on or before `ASTDT` and that either end on or after `ASTDT` or have no end date at all (still open), take the one with the latest start date. `DOSEON` is its `EXDOSE`. If there is no such record, `DOSEON` is missing (null).

Write one row per row of `ae_upstream`, identified by `USUBJID` and `AESEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 26

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

## Item 27

# ADVS: ONTRTFL (on-treatment record flag)

Derive `ONTRTFL`, the on-treatment flag, for the vital-sign measurements in `advs_upstream`. `ADT` is the measurement date, `TRTSDT` the subject's first dose date, `TRTEDT` the last dose date and `AVISIT` the analysis visit name.

`ONTRTFL` is `Y` when all of these hold:

1. `ADT` is on or after `TRTSDT`;
2. `TRTEDT` is missing, or `ADT` is on or before `TRTEDT` (the last dose day is included; there is no window after it);
3. it is not a pre-dose measurement: a measurement whose `AVISIT` is `Baseline` and whose `ADT` is the first dose day (`ADT` equals `TRTSDT`) is taken before the first dose, so it is **not** on treatment.

In every case where the flag is not `Y`, `ONTRTFL` is missing (null).

Write one row per row of `advs_upstream`, identified by `USUBJID` and `VSSEQ`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

## Item 28

# ADSL: TRTEDT (treatment end date)

Derive `TRTEDT`, the date each subject received their last study treatment: the end date `EXENDTC` of their last exposure record in `ex`. Missing if the subject has no usable exposure record.

Write one row for every subject in `dm`.

- Ambiguous? (yes/no): 
- Open point: 
- Confidence: 

