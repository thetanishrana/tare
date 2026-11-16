# Benchmark specification

## Unit of work: a derivation task

A task asks a programmer to derive **one target variable**, or a tightly coupled group such as `TRTSDTM` with `TRTSTMF`, in one ADaM dataset, from given inputs and a spec. Tasks are independent: any upstream variables needed are provided as inputs, taken from the oracle. That way one error doesn't cascade into later tasks, and every task can be scored on its own.

## Task definition format

One YAML file per task in `benchmark/tasks/`:

```yaml
id: adsl-saffl-std            # unique, stable
benchmark_version: 0.1
dataset: ADSL
target_vars: [SAFFL]
keys: [USUBJID]
therapeutic_area: core        # core | onco | vaccine | ophtha | neuro | peds
variant: std                  # std, or a sponsor-variant id, e.g. saffl-any-dose
perturbation: none            # none | dateshift4 | partial-dates | ... (see below)
oracle_id: std                # which oracle run holds the answer
inputs:                       # what the programmer may read
  - {name: dm, source: sdtm, columns: all}
  - {name: ex, source: sdtm, columns: all}
spec: specs/adsl-saffl-std.md # spec text, our own words
output_contract:
  columns: {USUBJID: string, SAFFL: string}
  allowed_values: {SAFFL: ["Y", "N"]}
difficulty: easy              # easy | medium | hard (initial guess; recalibrate with data)
error_categories_expected: [population-flag, placebo-zero-dose]
ambiguous: false              # true = the spec is deliberately underspecified
ambiguity_note: null          # if ambiguous: what's missing, and the correct escalation question
split: dev                    # dev | test | heldout
provenance: "admiral ADSL template; spec written by Tare"
```

## Where the answers come from (the oracle)

- **Standard tasks:** reference values come from running the admiral templates on unmodified `pharmaversesdtm`. K1 checks this reproduces `pharmaverseadam`. If small version differences show up, the regenerated output from our own pinned versions is the reference, not the package data.
- **Sponsor-variant tasks:** change the admiral call that derives the variable (a different cut point, window or flag rule), regenerate, and use that output. The spec text describes the variant rule. A memorized standard answer is then wrong unless the model actually follows the spec.
- **Perturbed-input tasks:** apply a perturbation to the SDTM data and regenerate. The programmer gets the perturbed inputs.
- **Record:** package versions (admiral, pharmaversesdtm, pharmaverseadam, R), the oracle script hash, and the perturbation parameters go in `data/oracle/<oracle_id>/manifest.json`.

## Sponsor variants (examples to build)

| Variable | Standard (admiral example) | Variant ideas |
|---|---|---|
| AGEGR1 | <18, 18–64, >64 | <65 / ≥65; <40 / 40–64 / ≥65 |
| SAFFL | Any qualifying exposure (dose > 0, or placebo at dose 0) | Requires at least 2 dosing records; excludes subjects missing an exposure end date |
| TRTEMFL | On or after first dose, within the study's window after last dose | Window +30 days versus +0 days; include AEs that worsened after dosing |
| ABLFL / BASE | Last non-missing value on or before first dose | Strictly before the first dose datetime; exclude unscheduled visits; average of screening and day-1 values |
| ASTDT imputation | admiral default for partial dates | Impute missing day to the 15th; never impute when only the year is known |
| LSTALVDT | Latest of AE, lab and treatment dates | Add vital-sign dates; exclude imputed dates |
| EOSSTT | From DS disposition | Treat "ONGOING" differently for subjects with a data cutoff |

Each variant has its own `oracle_id` and spec file.

## Perturbations

| id | What changes | Expected effect | Purpose |
|---|---|---|---|
| `dateshift4` | Every SDTM `--DTC` year +4 | Every ADaM date +4 years, everything relative unchanged | Metamorphic check of the oracle (K1); weak against memorization |
| `partial-dates` | Turn a sample of complete dates into partial ones | Imputation paths get exercised | Stress date handling |
| `unscheduled` | Add unscheduled visit records near baseline | Baseline and windowing logic gets exercised | Stress baseline rules |
| `same-day` | Add same-day duplicate measurements | Tie-breaking and ANL01FL logic | Stress ordering |
| `screen-fail` | Add screen-failure subjects with no exposure | Population flags | Stress SAFFL and EOSSTT |
| `edge-exposure` | Blank last dose dates, missing doses and partial start dates in EX (oracle id `pert-edge`; ADSL, ADAE and ADLB regenerated; perturbed EX saved with the oracle) | Open points in ambiguous specs about missing dose end dates, missing doses and partial dates start to change the output | Make those ambiguities measurable |
| `drop-ex` | Remove some exposure records | Treatment dates and durations change | Stress TRTSDT, TRTEDT, TRTDURD |

The oracle is regenerated after every perturbation, so answers are always exact.

## Memorization (contamination) controls

Frontier models have very likely seen the admiral templates and the CDISC pilot data. Controls:
1. **Sponsor variants:** a memorized standard answer fails.
2. **Perturbed inputs:** different values; anything memorized from the data is useless.
3. **Held-out therapeutic areas:** oncology, vaccine, ophthalmology and neuro datasets go only in the `heldout` split. No prompt tuning on them.
4. **Specs in our own words**, never pasted from implementation guides.
5. **Report results separately** for standard and controlled tasks. A large gap between them suggests memorization, which is a finding in itself.

## Ambiguity

- Every task gets an **ambiguity review**: would a competent clinical programmer need to ask a question? If yes, either fix the spec or mark the task `ambiguous: true` with the correct escalation question.
- Ambiguity is a first-class axis (decision of 2026-10-27, after the harder round). Aim for roughly 30% deliberately ambiguous tasks (about 45 of 150), each with a **matched clear twin** (same inputs and oracle, a spec that states the missing rule) where one exists, so the ask rate on ambiguous specs and the false-escalation rate on clear ones can be compared on the same derivation. The first set is in `benchmark/tasks/*-amb.yaml` (five tasks, round `k2b`).
- For ambiguous tasks the right behavior is to **escalate** with a precise question. Score escalation separately and don't count it as an error. Report three outcomes: escalated (good), answered matching the oracle's reading (right by luck: the choice was still unflagged), answered with a different reading (an unflagged divergence).
- The oracle holds one reading per task. Where several readings are defensible, record them in `ambiguity_note` and, as the benchmark grows, store the alternative answers so that "matches any defensible reading" can be reported next to "matches the oracle's reading". Alternative readings live in the task YAML (`readings:`), with reference solutions in `benchmark/reference/alt/` and keys built by `make alt-answers`; a reading is kept only if it changes the output on the data. Ambiguity labels so far were written by one author; before relying on them, have a clinical programmer rate a sample.
- Merck traced most of its remaining mismatches to ambiguous specs, so this split stops "errors" from being meaningless.

## Size and splits (target)

| Area | Tasks |
|---|---|
| ADSL | about 40 |
| ADAE and other OCCDS | about 35 |
| BDS (ADLB, ADVS, ADEG) | about 45 |
| Held-out therapeutic areas | about 20 |
| Ambiguous (spread across the above, with clear twins) | about 45 |
| **Total** | **about 150** |

- `dev` (about 30 tasks): tune prompts and harness settings here only.
- `test` (about 100): **frozen** before any reported run. Touch it only for final runs.
- `heldout` (about 20): reported separately. Never used for tuning. Built so far (2026-10-30): six ophthalmology tasks (oracle id `oph`, `r/ophtha.R`); no model has been run on them.
- Freezing means tagging the commit as `benchmark-v1.0`. After that, changes need a new benchmark version and a rerun of everything.

## Scoring

Per programmer output (or final harness output), per task:

| Class | Definition |
|---|---|
| **correct** | Output satisfies the contract, and every target value matches the oracle for every key (exact for strings and dates; numbers within `1e-8 × max(1, abs(x))`; NA equals NA) |
| **silent error** | Output satisfies the contract (runs, right columns and types, all keys present), but at least one target value differs from the oracle |
| **loud error** | No output, a runtime error after all repairs, or a contract violation (missing or extra keys, wrong columns or types) |
| **escalated** | (Harness only) the adjudicator escalated instead of choosing |

Also record per task: the number and share of mismatching records, which keys mismatch, and the **error category**.

**Error categories** (from `02_DOMAIN_PRIMER.md`, section 4): partial-date, date-vs-datetime, window-boundary, baseline-selection, join-duplication, population-flag, missing-value, derived-records, ordering-ties, units, category-order, spec-misread, other. Assign automatically where possible (a heuristic) and confirm by hand for a reviewed sample.

## The K2 seed kit (20 tasks)

The first 20 tasks are built in this format during week 1 (see `08_ROADMAP.md`, K2):
- 10 standard: suggested `TRTSDT`, `TRTDURD`, `SAFFL`, `AGEGR1`, `EOSSTT`, `LSTALVDT` (ADSL); `TRTEMFL`, `ASTDT` with `ASTDTF` (ADAE); `ABLFL`, `CHG` (ADLB).
- 10 variants of the same variables, using the variant ideas above.
- All in `split: dev`. They seed the full benchmark later.

## Versioning

- `benchmark/BENCHMARK_VERSION` holds a semantic version.
- Each run records the benchmark version and a hash of all task files.
- Oracle outputs are reproducible from scripts and pinned packages (renv lockfile). They aren't committed.
