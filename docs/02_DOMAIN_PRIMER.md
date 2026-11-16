# Domain primer: clinical trial data and QC

Read this before writing any derivation, spec or scorer. It covers what Tare needs and points to authoritative sources. Where exact rules matter, the installed **admiral templates and vignettes are the ground truth** for this project, not this primer.

## 1. The data pipeline

```
Case report forms / EDC (raw)
        │  mapping
        ▼
SDTM  (tabulation: what was collected, standardized)
        │  derivation  ← Tare lives here
        ▼
ADaM  (analysis: derived variables, flags, baselines, windows)
        │  reporting
        ▼
TLFs  (tables, listings, figures) → clinical study report → regulatory submission
```

- **CDISC** (Clinical Data Interchange Standards Consortium) defines these standards. Regulators such as the FDA expect standardized study data (SDTM and ADaM) in most submissions.
- **Define-XML** is the metadata that describes each dataset and variable, including derivation descriptions.
- **Double programming** is the classic quality control. A second programmer independently writes code from the same spec and the outputs are compared (`PROC COMPARE` in SAS, `diffdf` in R). Any difference is investigated. It's the long-standing gold standard but not a regulatory requirement, and many companies use risk-based mixes of independent programming, code review and self-QC (PharmaSUG 2025 MM-227).

## 2. SDTM essentials

SDTM organizes collected data into **domains**, one dataset each:

| Domain | Contents |
|---|---|
| DM | Demographics: one row per subject (age, sex, race, arm, reference dates) |
| EX | Exposure: drug administration records (dose, start and end dates) |
| AE | Adverse events (term, coded term `AEDECOD`, body system, start and end, seriousness, outcome) |
| DS | Disposition: study milestones and completion or discontinuation |
| LB | Laboratory results |
| VS | Vital signs |
| EG | ECG results |
| CM | Concomitant medications |
| MH | Medical history |
| SV | Subject visits |
| TS | Trial summary parameters |
| SUPPxx | Supplemental qualifiers: extra variables attached to a parent domain |

Key conventions:

- **Identifiers:** `STUDYID`, `USUBJID` (unique subject across the study), `--SEQ` (sequence number within subject and domain).
- **Dates are ISO 8601 character strings** in `--DTC` variables, and they **can be partial**: `2014-03`, `2014`, or `2014-03-05T10:30`. Partial dates are a major source of derivation errors.
- **Study day** (`--DY`) counts from the reference start date. Day 1 is the reference date and the day before is day -1. **There is no day 0.**
- `--STRESN` and `--STRESC` are standardized numeric and character results. `--ORRES` is the original result.
- Blanks: SDTM uses empty strings for missing character values. admiral workflows usually convert blanks to `NA` first (`convert_blanks_to_na()`).

## 3. ADaM essentials

ADaM datasets come in three main shapes:

### ADSL (subject level): one row per subject

Common variables. Exact derivations come from the admiral ADSL vignette and template:

| Variable | Meaning, as derived in admiral's ADSL example |
|---|---|
| `TRTSDTM` / `TRTSTMF` | Treatment start datetime and its imputation flag. From the earliest EX record with a valid dose (dose > 0, or dose = 0 for placebo) and a complete start date. Missing times are imputed. |
| `TRTEDTM` / `TRTETMF` | Treatment end datetime, from the latest qualifying EX record |
| `TRTSDT`, `TRTEDT` | Date parts of the above |
| `TRTDURD` | Treatment duration in days, from TRTSDT to TRTEDT |
| `TRT01P`, `TRT01A` | Planned and actual treatment for period 1 |
| `SAFFL` | Safety population flag: `Y` if the subject has a qualifying exposure record, otherwise `N` |
| `AGEGR1` | Age group. Example cut points: <18, 18–64, >64 |
| `REGION1` | Region from country |
| `EOSSTT` | End-of-study status (COMPLETED, DISCONTINUED, ONGOING), derived from DS |
| `EOSDT` | End-of-study date |
| `DCSREAS`, `DCSREASP` | Discontinuation reason and detail |
| `RANDDT` | Randomization date (from DS) |
| `DTHDT`, `DTHFL`, `DTHCAUS` | Death date, flag, cause (from AE with fatal outcome or from DS) |
| `LSTALVDT` | Last known alive date: the latest of several dates (AE starts and ends, lab dates, treatment end), with partial-date handling |

### BDS (Basic Data Structure): one row per subject, parameter and analysis timepoint

Used for ADLB (labs), ADVS (vitals), ADEG (ECG) and others. Key variables:

- `PARAMCD` / `PARAM`: the parameter code and description, such as a specific lab test with units.
- `AVAL` / `AVALC`: analysis value (numeric and character).
- `ADT`, `ADTM`, `ADY`: analysis date, datetime and study day.
- `AVISIT` / `AVISITN`: analysis visit, often from **visit windowing** rather than the collected visit.
- `ABLFL`: **baseline record flag**. Usually the last non-missing value on or before first dose. The rule details are a frequent source of errors.
- `BASE`, `CHG`, `PCHG`: baseline value, change and percent change from baseline.
- `ANRIND`, `BNRIND`: normal-range indicator (LOW, NORMAL, HIGH) for the record and at baseline.
- `ATOXGR`: toxicity grade (for example CTCAE), where applicable.
- `DTYPE`: derivation type for **derived records**, such as last observation carried forward. Rows with a DTYPE didn't exist in the source data.
- `ANL01FL`: analysis flag that chooses which record to use when several qualify.
- `ONTRTFL`: on-treatment flag.

### OCCDS (occurrence data): one row per event

Used for ADAE (adverse events), ADCM, ADMH. Key variables:

- `ASTDT` / `ASTDTF`, `AENDT` / `AENDTF`: analysis start and end dates and their **imputation flags** (which date part was imputed).
- `ASTDY`, `AENDY`: study days.
- `TRTEMFL`: **treatment-emergent flag.** Typically an AE that starts on or after first dose and within a window after last dose. The window length is study-specific and a classic source of variants and errors.
- `AOCCFL`, `AOCCPFL`, ...: first-occurrence flags used for counting subjects in tables.
- `ASEQ`: analysis sequence number.

## 4. Where derivation errors hide

Use this list to design tasks, variants and the error taxonomy:

1. **Partial dates:** which part to impute, imputing to the first or last of the period, and when not to impute.
2. **Date versus datetime:** same-day events before or after dosing; missing times.
3. **Windows:** treatment-emergent windows, visit windows, baseline windows (inclusive or exclusive edges, off-by-one errors).
4. **Baseline selection:** last value before first dose, ties on the same date, unscheduled visits, missing values.
5. **Joins:** many-to-one merges that duplicate rows; wrong keys; losing subjects.
6. **Population flags:** screen failures, subjects never dosed, placebo with zero dose.
7. **Missing values:** `NA` versus blank; comparisons with `NA` silently dropping rows.
8. **Derived records:** whether to create them, and setting DTYPE correctly.
9. **Ordering:** "first" and "last" depend on sort keys; ties broken by sequence numbers.
10. **Units and standardization:** the original versus the standardized result.
11. **Category lookups:** first-match order of conditions. admiral's docs note that catch-all conditions must come after specific ones.

## 5. pharmaverse and admiral

- **pharmaverse** is an open-source collection of R packages for clinical reporting.
- **admiral** builds ADaM datasets in R. It has therapeutic-area extensions: `admiralonco`, `admiralvaccine`, `admiralophtha`, `admiralneuro`, `admiralmetabolic`, `admiralpeds`.
- **Templates:** `use_ad_template(adam_name, save_path, package, overwrite, open)` writes a complete example script, for example for ADSL. `list_all_templates(package = "admiral")` lists them. Verified for admiral 1.5.0 (2026-10-12, `results/k1/summary.md`): the signature is `use_ad_template(adam_name, save_path, package, overwrite)` (no `open`). SDTM is read as `pharmaversesdtm::<domain>`; ADAE and ADLB read `admiral::admiral_adsl`, **not** `pharmaverseadam::adsl` (the two differ, notably `SAFFL` for screen failures); every template saves to a user-level cache directory (`tools::R_user_dir("admiral_templates_data", "cache")`) at the end.
- **Test data:**
  - `pharmaversesdtm` (v1.5.0 when checked, Apache-2.0): about 60 SDTM datasets. The core domains (dm, ae, ex, ds, lb, vs, cm, mh, sv, ts, supp*) are from or based on the CDISC pilot study, plus therapeutic-area sets (oncology, vaccine, ophthalmology, neuro, metabolic, pediatrics).
  - `pharmaverseadam` (v1.3.0 when checked, Apache-2.0): about 30 ADaM datasets produced by running the admiral templates on `pharmaversesdtm` data, regenerated by the package's `data-raw/create_adams_data.R` script. Includes adsl, adae, adlb, adlbhy, advs, adeg, adex, adcm, admh, adpc, adpp, adppk, adab, plus therapeutic-area datasets (adrs_onco, adtte_onco, adtr_onco, adce_vaccine, adis_vaccine, adbcva_ophtha, adoe_ophtha, advfq_ophtha, adapet_neuro, adtpet_neuro, adnv_neuro, adlb_metabolic, advs_metabolic, adcoeq_metabolic, advs_peds, adsl_vaccine).
  - **License trap:** `qs_metabolic` (and therefore `adcoeq_metabolic`) uses questionnaire content licensed only for not-for-profit use within admiral and pharmaverse examples. **Don't use either.**
- **Other useful packages:** `diffdf` (dataset comparison), `xportr` (SAS transport export), `metacore` and `metatools` (spec metadata), `tern`, `rtables` and `chevron` (tables).
- **Original CDISC pilot ADaM (VERIFY).** Merck's paper used the public CDISCPilot01 study, packaged as an "eSubmission Benchmark", with ADaM datasets ADSL, ADAE, ADTTE, ADLBC and ADADAS and well-structured specs. If the original pilot ADaM datasets and define.xml are publicly available with a usable license, they'd give a second answer key and realistic spec text. Find them and check the license before using.

## 6. CDISC CORE (optional)

The CDISC Open Rules Engine checks conformance to CDISC rules: structure, controlled terminology, required variables. `cdisc-rules-engine` on PyPI (0.17.1, released 2026-08-31, MIT) needs Python ≥3.12 and <3.13, a rules cache downloaded from its GitHub repo kept in sync with the package version, and a **CDISC Library API key** for controlled terminology and library metadata. It checks conformance, **not** value correctness. It's an optional extra for Tare.

## 7. Glossary

| Term | Meaning |
|---|---|
| ADaM | Analysis Data Model: analysis-ready datasets |
| SDTM | Study Data Tabulation Model: standardized collected data |
| TLF | Tables, listings, figures |
| BDS / OCCDS | ADaM dataset structures for measurements and for events |
| Spec | Variable-level derivation specification (often a spreadsheet, plus define.xml) |
| Double programming | Independent re-implementation and comparison for QC |
| Production / QC programmer | The one who writes the delivered code / the one who independently re-derives it |
| Treatment-emergent | An event starting after first dose (within a window) |
| Baseline | The reference value, usually the last before first dose |
| LOCF | Last observation carried forward (creates derived records) |
| Imputation flag | Records which date or time part was imputed (`D`, `M`, `Y`, `H`, ...) |
| Screen failure | Enrolled subject who never qualified or was never randomized |
| GxP | Good-practice regulations. Tare is not GxP software |
