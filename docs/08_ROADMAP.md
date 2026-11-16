# Roadmap, kill tests and risks

## Phases

Each phase ends with something publishable on its own, so stopping after any gate still leaves a finished project. Hours are estimates for a capable part-time builder working with Claude Code.

| Phase | Hours | Deliverable that stands on its own | Gate to continue |
|---|---|---|---|
| **0. Setup + kill tests** (week 1) | 12–15 | Working environment; K1–K4 results; go/no-go | K1 passes and K2 shows the problem exists (below) |
| **1. Benchmark** | 25–30 | About 150 controlled tasks, about 30% ambiguous with clear twins; silent-error and ask rates for at least 4 models (E0, E8 baseline); first post | Benchmark frozen as `benchmark-v1.0` |
| **2. Harness** | 25–30 | Double programming, isolation guard, comparator, adjudicator (including an assumptions check for choices every programmer makes the same way); E1–E6 and E8 results; **core result** | Results logged with confidence intervals; write-up drafted |
| **3. Training** (optional) | 30–40 | Small local model, SFT then GRPO; E7 | K4 signal exists; Phases 1–2 published |
| **4. Polish** | 10–15 | README, diff and adjudication viewer, write-up, video, posts | — |

Total: about 105–130 hours. Training can slip into winter break without hurting the core project.

## Week 1: kill tests

### K1: is the admiral oracle usable?

**Question:** do the admiral templates (1) regenerate `pharmaverseadam`, and (2) still run correctly on altered input?

**Procedure:**
1. Generate templates: `admiral::use_ad_template(adam_name = "adsl", save_path = "<path>", package = "admiral", overwrite = TRUE)`, and the same for `adae` and `adlb`. Verified for admiral 1.5.0: the function has no `open` argument. Result: K1 passed on 2026-10-12, see `results/k1/summary.md`.
2. **Read each template** and note how it reads input data (`pharmaversesdtm::x`, `pharmaverseadam::adsl`, `data()`, or a cache under `tools::R_user_dir(...)`) and where it writes output. Don't assume.
3. **K1a (reproduce):** run each template in a fresh R environment and compare its output with the corresponding `pharmaverseadam` dataset. Join on keys: ADSL on `USUBJID`; ADAE and ADLB on `USUBJID` + `ASEQ` if unique, otherwise fall back. Count mismatching records per variable. Write `diffdf` output to a log for details. Record package versions.
4. **K1b (metamorphic):** shift every SDTM `--DTC` value forward 4 years. Four years keeps leap days aligned, so ages, durations and study days don't change. Rerun the templates on the shifted data. **Expected:** perturbed output = baseline output with every date, datetime and `--DTC` value shifted +4 years. Compare.
5. Write `results/k1/summary.md`: per dataset, whether it ran, runtime, warnings, row counts, keys used, extra rows and columns, variables with mismatches (and how many records), and other differences (types, labels).

**Pass lines:**
- K1a: all three templates run, and most variables match. Small differences that trace to package versions are acceptable, but explain them. If many variables differ, use our own pinned regenerated output as the reference instead of the package data, and say so.
- K1b: all templates run on the shifted data, and the metamorphic relation holds exactly, or every exception has an explanation (for example, a hard-coded date in a template).

**If it fails:** fall back to static reference data plus hand-written Python reference implementations for the benchmark variables (about 15 extra hours), and shrink Phase 3 (fewer generated training tasks).

**Reference sketch (untested, adapt after step 2).** One way to swap in perturbed inputs without editing admiral's logic is to rewrite each template's data reads to go through shim functions:

```r
# Route all package data reads through shims we control
code <- readLines(template_path, warn = FALSE)
code <- gsub("pharmaversesdtm::([A-Za-z0-9_]+)", ".get_sdtm('\\1')", code)
code <- gsub("pharmaverseadam::([A-Za-z0-9_]+)", ".get_adam('\\1')", code)
writeLines(code, shimmed_path)

sdtm_override <- NULL      # named list of perturbed SDTM datasets, or NULL
adam_override <- list()    # e.g. list(adsl = our_generated_adsl)
.get_sdtm <- function(n) if (!is.null(sdtm_override) && n %in% names(sdtm_override)) sdtm_override[[n]] else getExportedValue("pharmaversesdtm", n)
.get_adam <- function(n) if (n %in% names(adam_override)) adam_override[[n]] else getExportedValue("pharmaverseadam", n)

# Year shift for ISO 8601 character dates (keeps partial-date structure)
shift_year_chr <- function(x, n) {
  ok <- !is.na(x) & grepl("^[0-9]{4}", x)
  x[ok] <- paste0(as.integer(substr(x[ok], 1, 4)) + n, substring(x[ok], 5))
  x
}
# For Date/POSIXct columns in outputs: lubridate::`%m+%`(x, lubridate::years(n))

env <- new.env(parent = globalenv())
source(shimmed_path, local = env)   # then read env$adsl, env$adae, ...
```

Watch for: templates that load data another way (step 2 tells you), templates that save outputs into a cache other templates then read, and `vapply` type strictness if you count mismatches that way. Run ADSL first and pass its output to the ADAE and ADLB runs, so the chain is consistent.

### K2: do frontier models make silent errors?

**Build the kit** (in the benchmark format, `04_BENCHMARK_SPEC.md`):
- 10 standard tasks: `TRTSDT`, `TRTDURD`, `SAFFL`, `AGEGR1`, `EOSSTT`, `LSTALVDT` (ADSL); `TRTEMFL`, `ASTDT` with `ASTDTF` (ADAE); `ABLFL`, `CHG` (ADLB).
- 10 sponsor variants of the same variables, each with its own oracle run.
- Each task has a spec in our own words, input parquet files, a data description, an output contract, and an answer key (hidden).
- A prompt template asking for a complete R (or Python) script that reads `inputs/` and writes `out/result.parquet`.
- A scoring script that runs each response in the sandbox and classifies it as correct, silent error or loud error, using the same comparator as the harness.

**Run modes (ask the project owner which one):**
- **API:** Claude Sonnet 5.5 and Haiku 5.5, 1 sample each, single-shot plus up to 2 repairs for loud errors. Expected cost about $1 (estimate before running).
- **Manual:** The project owner pastes each prompt into the Claude and ChatGPT apps (memory off, a fresh chat each time) and saves each response as `k2/responses/<model>/<task_id>.md`. The scoring script extracts the code block.
- Also run `qwen3-coder:30b` locally if it's pulled (free). It feeds K3.

**Pass line:** at least **3 of 20** tasks are silent errors for at least one frontier model. Expect most errors to be on the variant tasks.
**If it fails:** add harder derivations (visit windowing, last-observation-carried-forward records, baselines with unscheduled visits, partial-date imputation variants). If those also come in near zero, drop "silent error rate" as the headline and reposition Tare around the local and firewall setting plus cost (frontier-grade correctness from local models).

### K3: are errors correlated? (informational)

From K2 (plus the local model): for each pair of models, compute P(B wrong ∣ A wrong) and the same-wrong rate (identical incorrect output). With 20 tasks this is anecdotal. It's a signal, not a result.

### K4: does a small local model have any signal?

- Run `qwen2.5-coder:7b` (or a Qwen 1.7–4B model) on the 20 tasks, 3 samples each.
- **Pass line:** some correct answers (ideally 10–50% across samples). That's enough signal for SFT and GRPO.
- **If it fails** (near 0%): Phase 3 becomes SFT only, on reference code, or is dropped. The core project is unaffected.

### Go/no-go template (write into `STATUS.md`)

```
Date:
K1: pass/fail. One line on why.
K2: N/20 silent errors (Sonnet), N/20 (Haiku), N/20 (qwen3-coder). Where the errors cluster:
K3: same-wrong observations:
K4: correct share across samples:
Recommendation: GO / GO with changes (list) / NO-GO (why)
Changes to the plan:
```

## Status after the kill tests (2026-10-27)

K1 passed; K4 passed; K2 failed its pass line as written (0 of 20 silent errors for both frontier models). The harder round (`results/k2b/summary.md`) showed that silent errors come from ambiguous specs, that no model asks, and that agreement across models is not correctness. **GO with changes** was approved on 2026-10-27: reposition around ambiguity and what catches it (`docs/STATUS.md`, go/no-go; `docs/09_DECISIONS.md`). Phases below are re-scoped accordingly.

## Phase 1: benchmark (outline)

1. Write the oracle variants and perturbation scripts (R), with manifests.
2. Write task YAMLs and specs for about 150 tasks, about 30% ambiguous with clear twins (the five `*-amb` tasks are the seed). Do the ambiguity review, with an external rating of a sample. Assign splits.
3. Task-bundle builder and data-description generator, tracking token counts.
4. Run E0 on dev with local models; fix task bugs; freeze `benchmark-v1.0`.
5. Run E0 on test and heldout (local models free; Claude through batch).
6. First post: silent-error rates, with confidence intervals and the error taxonomy.

## Phase 2: harness (outline)

1. Sandbox and isolation guard with tests (first, not last).
2. Comparator and scorer, shared code.
3. Double-programming runner, adjudicator with JSON verdicts, escalation questions.
4. E1–E6 on dev, then freeze prompts; final runs on test and heldout.
5. Report: main table, cost against escaped-error chart, correlation heatmap, case studies.

## Phase 4: polish (outline)

- README with the headline result, a GIF or screenshot of the diff and adjudication viewer, quickstart, reproducibility commands.
- Write-up (blog post or PDF).
- A clear limitations section.

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Frontier models make too few errors | Medium | High | Variants and harder derivations; K2 pass line; repositioning plan above |
| Memorization of the public pilot data and templates | High | Medium | Variants, perturbations, held-out therapeutic areas, standard vs controlled reporting |
| Correlated errors erase the harness gains | High | Medium | Cross-family and cross-language diversity; a negative result is still publishable |
| Ambiguous specs make "errors" meaningless | Medium | High | Ambiguity review; labeled ambiguous subset scored separately |
| ADaM learning curve | Medium | Medium | Start from admiral vignettes; limit to ADSL, ADAE, BDS |
| Oracle won't regenerate on perturbed data | Low–Medium | Medium | K1 decides; static fallback |
| Training shows no gain | Medium–High | Low | Optional phase; SFT first; honest reporting |
| Schedule collision with finals | Medium | Medium | Gated phases; training can move to winter break |
| Overclaiming to a pharma audience | Medium | High | Honest-framing lines in `01_PROJECT_BRIEF.md`; never "validated" or "compliant" |
| License or terms slip | Low | High | Rules in `CLAUDE.md` |
| API overrun | Low | Low | Local-first development; ask above $2; Console spend limit |

## Stop rules

- If K1 and the fallback both fail: stop and rethink the data source with the project owner.
- If K2 and the harder-derivation retry both show almost no silent errors: switch to the repositioned framing (local and firewall correctness plus cost). Don't push the original headline.
- If any phase runs more than 50% over its hours: stop, record why in `STATUS.md`, and agree a cut with the project owner.
