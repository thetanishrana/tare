# K1: is the admiral oracle usable?

**Result: PASS (K1a with one explained difference, K1b exact).** Run date 2026-10-12. Reproduce with `Rscript r/k1_oracle_check.R` from the repo root (about 45 s). All numbers below come from `results/k1/k1_results.json`; diffdf output is in `results/k1/logs/`.

Versions: R 4.6.1, admiral 1.5.0, pharmaversesdtm 1.5.0, pharmaverseadam 1.3.0, diffdf 1.1.2, dplyr and lubridate as in `session_info.txt`.

## What the templates actually do (step 2: read, not assumed)

- `use_ad_template()` in the installed admiral has **no `open` argument** (signature: `adam_name, save_path, package, overwrite`). The doc's example call was wrong for this version; `07_SETUP.md` and `08_ROADMAP.md` need the fix.
- SDTM is read as `pharmaversesdtm::<domain>` (ADSL: dm, ds, ex, ae, lb; ADAE: ae, ex; ADLB: lb).
- **ADAE and ADLB do not read `pharmaverseadam::adsl`. They read `admiral::admiral_adsl`**, a separate packaged ADSL. It differs from `pharmaverseadam::adsl`: no `BRTHDTC`, and `SAFFL` is `NA` instead of `N` for 52 of 306 subjects (the screen failures).
- Every template ends by saving to `tools::R_user_dir("admiral_templates_data", "cache")`, a user-level cache outside the project. The runner cuts each template at its "Save output" block, so nothing is written there.
- Templates define helper functions (for example `format_eosstt`) that admiral evaluates in the global environment, so each template must run as a top-level script. The runner runs each one in its own fresh `Rscript` process (`r/run_template.R`).

## K1a: do the templates regenerate `pharmaverseadam`?

Shipped templates, run in a fresh process, no warnings. Compared on shared columns, joined on the keys shown.

| Dataset | Runtime | Rows (pkg / template) | Keys | Variables with mismatches | Extra columns in template output |
|---|---|---|---|---|---|
| ADSL | 1.5 s | 306 / 306 | USUBJID | **0 of 55** | ARMNRS, ACTARMUD |
| ADAE | 1.9 s | 1191 / 1191 | USUBJID + AESEQ | **3 of 107**: LDOSEDTM (299 records), DOSEON (295), DOSEU (295) | none |
| ADLB | 6.1 s | 83652 / 83652 | USUBJID + ASEQ | **0 of 115** | none |

Keys: the package ADAE has no `ASEQ` column, so ADAE uses `AESEQ` (unique per subject). ADLB uses `ASEQ` (unique). No rows are missing or extra in any dataset.

**The ADAE differences are real but explained in part.** The installed template first expands EX into single-day records (`ex_single`), then sets `LDOSEDTM` to the last dose start on or before the event, so a dose on the event date counts. The packaged ADAE reports the previous record's end date instead and leaves `DOSEON` and `DOSEU` missing in those rows (example: subject 01-701-1028, AE start 2013-08-08: package `LDOSEDTM` 2013-08-01, template 2013-08-08 with dose 81 mg). So the package data was built with different last-dose logic from the installed template. **Not verified:** why. The package's `data-raw` build script isn't in the installed package, so I haven't confirmed whether it's a version difference or a deliberate choice.

**Other differences (not value differences):**
- The packaged datasets carry variable labels that raw template output lacks (label differences: ADSL 30, ADAE 85, ADLB 93 variables). Two ADSL labels differ in wording (TRT01P, TRT01A). Types match for every shared column.
- `admiral_adsl` differs from `pharmaverseadam::adsl` (`SAFFL` on 52 rows; `BRTHDTC` absent), as described above.

## K1b: metamorphic test (shift every SDTM `--DTC` forward 4 years)

17 character `--DTC` columns shifted across dm, ds, ex, ae and lb (list in the JSON, `sdtm_cols_shifted`). Baseline and perturbed runs are chained: ADSL first, and its output feeds ADAE and ADLB. The expected output is the baseline with every Date, datetime and `--DTC` column shifted +4 years.

| Dataset | Rows | Variables mismatching the expected shifted baseline | Control: unshifted baseline vs perturbed |
|---|---|---|---|
| ADSL | 306 | **0 of 57** | 18 variables differ (all date-related) |
| ADAE | 1191 | **0 of 110** | 25 variables differ (all date-related) |
| ADLB | 83652 | **0 of 118** | 19 variables differ (all date-related) |

The relation holds exactly, with no exceptions. The control shows the check can fail: without the expected shift, only date variables differ, and every non-date variable (flags, study days, durations, categories) is identical between the baseline and shifted runs. A grep of the three templates found no hard-coded dates, `ymd()`/`as.Date()` calls or `Sys.Date()`/`Sys.time()` calls, which is consistent with the exact result.

Runtimes (baseline, perturbed): ADSL 1.5 s, 1.4 s; ADAE 1.9 s, 1.8 s; ADLB 5.9 s, 6.3 s. No warnings.

## Consequences for Tare

1. **Use Tare's own pinned, regenerated output as the oracle reference, not `pharmaverseadam`.** K1a is a pass, but ADAE differs in 3 variables and the chained run is the one that supports perturbed inputs. This matches the roadmap's fallback wording ("use our own pinned regenerated output ... and say so").
2. **Chain ADSL into ADAE and ADLB** instead of letting them read `admiral_adsl`. That is what K1b did, and perturbed-input runs need it.
3. The shim approach works: redirecting `pharmaversesdtm::x` reads and the ADSL read, and cutting the save block, is enough. Running each template in a fresh process is required.
4. Caveats: this tests three templates on one study's data. It says the oracle is usable for ADSL, ADAE and ADLB, not that it's correct for derivations the templates don't cover (for example sponsor variants, which need modified templates and their own checks).
