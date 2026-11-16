# Decision log

Newest first. Each entry: decision, why, and what would change it. Claude Code: append new decisions here instead of re-arguing old ones.

## 2026-11-06: E9 (reviewer on unseen ambiguous tasks) design, fixed before any task is built or run

- **Why:** the reviewer's blind spot is the shared stated assumption (first-dose-day boundary cases passed in H4, H4b and H4c), but H5 could not test it because the held-out programmers asked themselves (0 would-be silent errors, minimum 10). The dev logs show where the programmers stay quiet: on 11 of the 21 ambiguous dev tasks the Claude pair never asked in 3 samples (`adae-astdt`, `adae-astdt-pdates`, `adae-trtemfl`, `adlb-chg`, `adlb-ontrtfl`, `adlb-ontrtfl-edge`, `adlb-pchg`, `adsl-saffl`, `adsl-saffl-edge`, `adsl-trtsdt`, `adsl-trtsdt-edge`), and most of them are boundary or convention questions (is the day of first dose inside the window, which record counts as baseline).
- **Question:** on ambiguous tasks the programmers do not flag themselves, how many silent errors does a reviewer catch, and does the competing-readings reviewer (R2, `REVIEWER_PROMPT_V2`, unchanged) catch the shared-stated-assumption cases that the assumptions reviewer (R1, `REVIEWER_PROMPT`) passes?
- **New set, not part of v1.0:** round `u1`, split `unseen`, kept out of `benchmark-v1.0`. It becomes v1.1 only by a later decision. Target 12 ambiguous tasks, each with a clear twin (24 tasks). Candidate families, all boundary or convention choices a careful programmer could read two ways: reference-day boundary for an on-treatment flag on vital signs (`advs`); age group edges at exactly 65 (`adsl`); day-count convention for an end day relative to first dose (`adae`); rounding rule at a stated number of decimals for derived vital-sign values (`advs`); baseline choice when a time point has two pre-dose records; the study-completion date used as an end date when no last dose exists. Specs are written in our own words.
- **Admission rules for a task (all checked by script before any model sees it):** the oracle reading and at least two stored readings each differ from every other on the data (`scripts/build_alt_answers.py` already flags readings identical to the oracle); the clear twin's reference passes `make references`; the readings are written before any model run on the set. Task authorship is single-author and written by Claude after seeing which families the programmers stay quiet on, so the set is not independent of the dev findings; say so in any result.
- **Screening step (programmers only, no reviewer):** one sample of Haiku 5.5 and Sonnet 5.5 as single programmers on the ambiguous tasks only. Tasks where either programmer escalates are dropped from the confirmatory set (they cannot test the reviewer) and reported. The screening sample is not reused as a confirmatory sample. If fewer than 8 tasks remain after screening, extend the set (new tasks in the quiet families) before any pair run, and say so.
- **Confirmatory run:** programmers Haiku 5.5 (A) and Sonnet 5.5 (B), Python, prompt `k2-v4`, adjudicator Sonnet 5.5, 3 fresh samples per remaining task and twin. R1 live; R2 and reviewer-off by replay on the same logged programmers. No prompt, task, reading or reviewer change after the first confirmatory result.
- **Definitions (as in E8c):** a *would-be silent error* is an ambiguous pair whose programmers agree, nobody asked, and which the reviewer-off replay scores `silent_error`; a *false alarm* is a clear-twin pair the reviewer escalates when the programmers agree and nobody asked. A *shared-stated-assumption pair* is a would-be silent error where both assumption lists state the same choice.
- **Hypotheses:** H1: R1 escalates on at least 50% of the would-be silent errors with at most 5% false alarms (the H4 to H4c level was about 60% and 2%). H2: R2 escalates on strictly more would-be silent errors than R1. H3: R2 escalates on at least half of the shared-stated-assumption pairs. H4 (reported whatever the outcome): R2's false-alarm rate on clear pairs, where H5 found 16 of 36 against 3 of 36 for R1; a higher catch rate bought with that many false alarms is not a win, so report catch rate and false-alarm rate together, not either alone.
- **Power rule:** a claim needs at least 10 would-be silent errors (and at least 5 shared-stated-assumption pairs for H3); below that, report raw counts as underpowered, as in H5.
- **Cost estimate (not spent, needs a go-ahead):** screening about $0.3; pair run on 24 tasks x 3 samples = 72 pairs at about $0.02 per pair, about $1.5; R2 replay about 3x the reviewer cost of R1, about $0.5; total about $2.3, over the $2 line, so ask before starting, and ask again before any run beyond this plan. Building tasks, oracles and the admission checks is free.
- **Outside rating:** the new pairs get a blinded rating sheet like the v1.0 pairs, so an external rater can check the ambiguity labels of this set first if one is available.
- **Build log (2026-11-06, free, no model run):** 6 of the target 12 pairs built so far: `advs-ontrtfl`, `advs-anl01fl`, `adsl-trtedt-edge` (perturbed exposure data), `adlb-r2base`, `advs-avisit`, `advs-ady`; 2 or 3 stored readings each, every reading checked to differ from the oracle on real records (smallest difference 13 of 306 subjects, `adsl-trtedt-edge` any-record), clear twins and references all score correct (`make references` 91 of 91, which includes the 79 v1.0 tasks). Families differ from the plan above: no rounding, age-edge or two-baseline-records task, because the public data has no values at those edges or the oracle has no column for them. Candidates tried and dropped because the readings gave identical output on this data: `advs-bnrind`, `adlb-anl01fl`, `adlb-lvotfl`, `adae-aendy`; also dropped from `advs-ontrtfl` the readings `after-first-dose-day` and `missing-end-excluded` (identical output). Answer keys are the admiral oracle columns, checked against the clear spec's rule before the spec was kept. The v1.0 tag is unaffected; the working tree now holds 91 tasks. Blinded rating sheet for these pairs: `docs/ratings/rating_sheet_u1.md` (key in `rating_key_u1.md`, never show raters the key). Still to do: the screening step (needs a go-ahead, about $0.3) and, if fewer than 8 ambiguous tasks pass screening, more tasks before any pair run.

## 2026-11-16: Repository history squashed for the public release

- The development history was squashed into a single commit before the repository was made generally available, so earlier commits are not visible. The tag `benchmark-v1.0` was re-created on that commit: the v1.0 benchmark is every task except those in round `u1` (split `unseen`), which were added later and are kept outside the tag. `manifest.json` files under `results/` record the git commit of the run; those hashes refer to the pre-squash history and no longer resolve.

## 2026-11-11: E9 result: R1 under the bar, R2 catches everything by asking nearly always

- `results/e9/summary.md` ($1.80; the R2 replay overran its estimate by about $0.35). 7 tasks (not the pre-registered 8; the run went ahead on 7), 42 pairs, 12 would-be silent errors from 4 tasks. H1 not met (R1 5 of 12, 0 of 21 false alarms), H2 not met (R2 12 of 12 but 12 of 21 false alarms), H3 met with an unchecked caveat, H4 reported (R2 asks on 33 of 42 pairs). No change to the harness default: R1 stays the optional check, R2 is not adopted.
- What this adds to the claims: on a new set of ambiguous tasks the assumptions reviewer again caught a minority-to-half of the would-be silent errors with no false alarms, and again missed shared stated assumptions; a reviewer that must name competing readings catches them but asks on most clear specs too. Claims must carry the limits: 7 tasks, 4 contributing, 3 correlated samples each, same-family pair, tasks authored after seeing where the programmers are quiet.

## 2026-11-11 (latest): two more tasks built and dropped; new oracle id `pert-edge-adae`

- `adlb-ablfl-edge` (Haiku asked) and `adae-lastdose-edge` (both asked) were built and screened; both dropped. Kept stays at 7 of 14 built; the three attempts after the first seven were all dropped, so returns are diminishing: the tasks that stay quiet are the ones whose edge case sits in missing dates or a boundary the spec wording does not hint at, while multi-part exposure rules and anything with several visible edge cases draw questions.
- Added the oracle id `pert-edge-adae` (`r/oracle_build.R`): the ADAE for the pert-edge exposure perturbation with the perturbed EX also passed as SDTM input. The existing `pert-edge` ADAE had LDOSEDTM and DOSEON built from the unperturbed EX; no v1.0 task uses those columns on `pert-edge`, so v1.0 is unaffected.
- Spend for these two tasks $0.0362; total $8.12.

## 2026-11-11 (later): option 1 chosen; the 12th pair also dropped at screening

- The decision was to build one more task rather than run on 7. `adlb-ablfl-edge`-style ports were out (one reading); `adsl-trtdurd` has one reading and drew questions on the standard data, so it was not built. `adae-aoccifl-aedates` was built (references correct; readings differ on 70, 230 and 414 of 1191) and screened: Haiku asked, so it is dropped. Kept: still 7. The minimum of 8 is unchanged; next task to be built in a fresh session. No pair run started. Cost of this step $0.0149; total spend $8.08.

## 2026-11-11: E9 set extended to 12 pairs built, 7 kept after screening

- Added `advs-ontrtfl-edge`, `advs-ablfl-edge`, `adae-trtemfl-pdates`, `adae-astdy-pdates`, `advs-chg-edge` (all with clear twins; references 101 of 101 correct, every stored reading differs from the oracle) and the oracle id `pert-edge-advs` (the pert-edge exposure perturbation with ADVS regenerated; `r/oracle_build.R`; the existing pert-edge files are byte-identical). Dropped before screening: `adlb-ablfl-edge` (one reading only); `adae-lastdose-edge` was not built because the std rule does not reproduce the oracle on the perturbed data (1126 of 1191 LDOSEDTM values differ; not investigated).
- Screening (`results/u1_screen/summary.md`, $0.0765 for these sets): `advs-chg-edge` dropped (both programmers asked). Kept in all: 7 (`advs-ontrtfl`, `adsl-trtedt-edge`, `advs-ady`, `advs-ontrtfl-edge`, `advs-ablfl-edge`, `adae-trtemfl-pdates`, `adae-astdy-pdates`), one short of the 8 required, and two of the 7 were answered correctly by both programmers.
- Finding worth keeping whatever E9 shows: on the perturbed-data tasks the two programmers gave the same wrong output with no stored reading matching (`advs-ontrtfl-edge`, `adae-trtemfl-pdates`): hidden edge cases (missing dates) are resolved identically and silently. Stored readings were not extended after seeing this (pre-registered).
- Open: build one more quiet-family task, or run E9 on 7 tasks with the deviation from the pre-registered minimum written next to the result. No pair run started.

## 2026-11-08: E9 screening result: 3 of 6 tasks kept, set must be extended

- `results/u1_screen/summary.md` ($0.09). Under the rule fixed on 2026-11-06, tasks where either programmer asked are dropped: `adlb-r2base-amb` (Haiku asked), `advs-avisit-amb` (Haiku asked), `advs-anl01fl-amb` (both asked). Kept: `advs-ontrtfl-amb`, `adsl-trtedt-edge-amb` (both programmers silent and wrong in the screen), `advs-ady-amb` (both correct, so unlikely to give would-be silent errors). That is 3, below the 8 required, so the set is extended before any pair run. The dropped tasks stay in the repository and are reported, not edited.
- Lesson for building more: the quiet tasks are the on-treatment boundary and the exposure-date rules; the ones that drew questions had a visible edge case in the data (a zero baseline, odd visit names, several records on one date). New tasks should hide their edge case in plain sight, with the same kind of rule that `advs-ontrtfl` and `adsl-trtedt-edge` use, or on other datasets for the same rule.

## 2026-11-06: Benchmark frozen as v1.0 (tag `benchmark-v1.0`)

- Agreed on 2026-11-06. Contents at the tag: 79 tasks (29 ambiguous, 28 of them with a clear twin, 61 stored readings; 73 dev, 6 held-out ophthalmology); `make references` 79 of 79, `make test` 50 passed.
- What the freeze means: task specs, oracles, stored readings and answer keys do not change under this tag. Corrections or additions go into a new tag (v1.1) with the reason recorded here, and results are reported against the tag they ran on. The held-out rule stands: no tuning on those 6 tasks.
- Stated limits of v1.0: well short of the 150-task target; ambiguity labels and stored readings are single-author with no external rating (the blinded sheet `docs/ratings/rating_sheet.md` is unused); some readings were added after seeing model outputs; the 11 p1g/p1h tasks have only a one-sample spot check; the held-out slice was run once (H5).
- Also fixed the same day: run directories now get a suffix when two runs start in the same second (a replay test failed intermittently for this reason).

## 2026-11-06: H4c, a third sample, agrees with H4 and H4b

- `results/h4c/summary.md` ($0.90): check off 10 silent errors on the 21 ambiguous tasks, check on 3; 0 of 20 clear false alarms. Over three samples 24 to 8. The first-dose-day cases passed again, so the blind spot stands. No change to the harness design or the claims; the write-up's two-sample numbers still need updating to three.

## 2026-11-04: E8c result: underpowered, and v2 over-asks

- `results/h5/summary.md`. On the held-out ophthalmology slice the programmers asked on 18 of 20 ambiguous pairs, leaving 0 would-be silent errors for a reviewer to catch (needed: 10); H1 to H3 cannot be confirmed. Reviewer v2 asked on 16 of 36 consulted clear pairs against 3 of 36 for v1, so on the evidence of the clear pairs v2 is worse and is not adopted.
- Cost overran the estimate ($2.02 against about $1.5, the v2 replay alone $0.92). Lesson for estimates: reviewer v2 replies are long JSON (about 3x the cost of v1 reviews).
- Decision: the harness default stays reviewer v1 as an option, off in headline runs. No change to v2 on these results (held-out rule). To test whether a competing-readings reviewer can catch shared-assumption misses, the next design needs ambiguous tasks where the Claude programmers do not ask themselves; these are the first-dose-day boundary cases on dev tasks, so a new unseen set would have to be built. Not started.
- Paid runs from here are small.

## 2026-11-04: E8c (competing-readings reviewer) design, fixed before any run

- **Question:** H4 and H4b showed a Sonnet reviewer of the assumption lists asks on about two thirds of the pairs that would otherwise be silent errors, with almost no false alarms, but passes the cases where both programmers state the same reading with a reason. Does a reviewer that must write out the competing readings of each choice, and whether each would change the output, catch those too?
- **Reviewers compared on the same logged programmers (replay, so the programmers run once):** R1, the existing `REVIEWER_PROMPT` (control). R2, new `REVIEWER_PROMPT_V2` in `tare/prompts.py`, written now and not tuned: the reviewer lists every distinct choice in either programmer's list, writes the competing readings a careful programmer could take from the spec alone, says whether the spec's text settles the choice (and that two programmers agreeing does not settle it), and whether choosing differently would change which records get which values (`yes`, `no` or `unknown`). It replies with JSON. **The escalation rule is in code, not left to the model:** escalate if any choice has `spec_settles` false and `changes_output` not `no`; the question is the first such choice's question. The model's own `escalate` field is ignored. Both reviewers are Claude Sonnet 5.5, no sampling parameters.
- **Primary evaluation (held-out, frozen):** the six ophthalmology tasks (`ho1`), programmers Claude Haiku 5.5 (A) and Sonnet 5.5 (B), Python, prompt `k2-v4`, adjudicator Sonnet 5.5, **10 samples per task** (60 pair runs). Nothing about the prompts, readings, specs or tasks is changed after seeing any of these results. Only 2 of the 6 tasks are ambiguous, so the number of agree-and-wrong pairs may be small; the run is therefore sized by samples, not tasks.
- **Definitions:** a *would-be silent error* is an ambiguous pair whose programmers agree, nobody asked, and which the replay with the reviewer off scores `silent_error`. A *false alarm* is a clear-twin pair the reviewer escalates when the programmers agree and nobody asked.
- **Hypotheses (paired on the same logged pairs):** H1: R2 escalates on at least 70% of the would-be silent errors and on at most 10% of the clear pairs. H2: R2 escalates on strictly more would-be silent errors than R1, and not on more than 5 percentage points more clear pairs. H3: R2 escalates on the shared-stated-assumption pairs (programmers' lists state the same choice) that R1 passed. A claim is made only if there are at least 10 would-be silent errors; below that the result is reported as underpowered with the raw counts.
- **Exploratory, not confirmatory:** replaying R2 over the dev logs of H4 and H4b (cents). Those logs were used to find the blind spot, so a good result there is not evidence; it only checks that R2 does not collapse (for example by asking on every clear pair).
- **Cost:** estimated about $1.5 for the held-out run (60 pair runs about $0.8, R1 and R2 reviews on roughly 40 agreeing pairs about $0.6, adjudications a few cents); confirm before running because it is close to the $2 line. Programmer responses are logged, so reviewer variants can be added by replay for cents.
- **Limits stated in advance:** a same-family pair; two ambiguous tasks; the oracle for the slice is our own admiral-function script; labels and readings by one author; one reviewer model.

## 2026-10-30: Held-out slice: ophthalmology only, built with base admiral

- Ophthalmology only was chosen, with the installed admiral (no extension packages). Other areas in `pharmaversesdtm` are tiny (vaccine 2 subjects, peds 5, onco 8, neuro 15) and would need `admiralvaccine`, `admiralpeds`, `admiralonco` or `admiralneuro` for oracles that are not our own code.
- Oracle: `r/ophtha.R` applies admiral derivation functions (`derive_var_extreme_flag`, `derive_var_base`, `derive_var_chg`, `derive_vars_merged`) to the ophthalmology SDTM; oracle id `oph`. It is not an admiral template, so the oracle is less independent than the ADSL, ADAE, ADLB and ADVS ones; the Python reference solutions were written separately and all score correct on it.
- Six tasks, round `ho1`, split `heldout`. Rule fixed now: no prompt, reading or spec tuning on these tasks. The first model run on them uses frozen prompts and the harness configuration chosen from the dev tasks. The planned competing-readings reviewer test (see the H4b decision) is run on this slice.
- Ambiguity labels and stored readings for the three `-amb` tasks are single-author, as elsewhere.

## 2026-10-29: H4b replicates H4; the blind spot is a shared stated assumption

- Second sample (`results/h4/summary.md`, `results/h4b/`): the Sonnet reviewer again asked on about two thirds of the would-be silent errors (5 of 7) and on none of 20 clear pairs; over two samples silent errors went from 14 (check off) to 5 (on). The same two cases passed both times, with both programmers stating the same reading.
- Decision: the assumption check is part of the harness design for Claude programmers, reported next to the no-check pipeline. Next experiment, pre-registered before it runs: a reviewer variant that must name the competing readings and say whether each changes the output, tested on pairs not used to find this blind spot (a new sample of tasks or the held-out slice).

## 2026-10-29: H4: with Claude programmers the assumption check discriminates

- `results/h4/summary.md`. 41 pairs, Haiku + Sonnet programmers, Sonnet reviewer and adjudicator: the reviewer escalated 7 of 12 reviewed ambiguous pairs and 1 of 20 clear ones, and silent errors on ambiguous tasks fell from 6 (check off, by replay) to 2. It still missed the first-dose-day boundary in `adae-trtemfl-amb` and `adlb-ontrtfl-amb`.
- Decision: keep the assumption check in the harness design as an option to be reported next to the no-check pipeline, with these numbers marked as one sample on a same-family pair. This supersedes the H3 decision to keep it off in headline runs, for Claude programmers only; the local-model result (H2, H3) still does not support it. Next evidence needed: more samples, a cross-family pair, and the missed boundary cases.

## 2026-10-29: H3: the assumption check tested in isolation, inconclusive

- `results/h3/summary.md`. Replaying the H2 programmers with four different reviewers (and none): of 5 pairs that reach the reviewer, gpt-oss:20b caught both silent errors and flagged 2 of 3 clear pairs, Sonnet caught 1 and flagged the same 2, Haiku caught none and flagged them too, qwen3-coder:30b asked on nothing. No reviewer discriminates on this sample.
- Decision: keep the assumption check optional and off in headline runs until a larger test exists. The test needs many pairs where both programmers agree on an unflagged choice and several samples, ideally with Claude programmers. `replay_from` makes reviewer comparisons cheap (programmers run once).

## 2026-10-29: H1 and H2 (first harness runs): what they say about the design

- H1 (local adjudicator, no check): agreement hid 2 of 6 wrong ambiguous outputs (both programmers made the same unflagged choice), the adjudicator picked wrong sides twice. H2 (v4 prompt, Sonnet adjudicator and reviewer): 5 of 6 ambiguous pairs escalated but also 3 of 6 clear twins. Comparator-agreement alone is not evidence of correctness, as designed for; the assumption check is not yet shown to discriminate (1 catch, 2 false alarms, 1 miss).
- Decision: keep the assumption check optional and next test it in isolation (programmers fixed on v4, reviewer on and off, a Claude and a local reviewer, same pairs), because H2 changed prompt, adjudicator and check at once. Do not report H1 or H2 as measurements: 12 pairs, 1 sample.

## 2026-10-29: Phase 2 harness core built, with the assumption check as a configurable hypothesis

- Built `tare/programmer/agent.py` (one programmer: prompt, sandbox, repairs, returns the output frame and the assumptions list), `tare/adjudicate.py` (JSON verdict; malformed replies become escalations, so a parse failure hands the case to a human and never picks a side) and `tare/harness.py` (`run_pair`, `score_harness`). The scorer is only used after the run, on the final output.
- Isolation by construction: programmer and adjudicator modules import neither the scorer nor the oracle; a unit test checks the import lists. Programmers and adjudicator see their own stderr, the contract problems and (adjudicator) the diff between the two outputs, never the oracle.
- The assumption check is optional (`reviewer=None` disables it) because E8b gave no evidence yet that a reviewer can tell consequential assumptions from harmless ones. It stays a hypothesis for the first harness experiments.
- Tested end to end with fake clients and the real sandbox (agree, disagree with each verdict, programmer escalation, assumption check). No real-model harness run yet. Next: a config and `tare run` support for pairs, R programmers, and a first small run on local models.

## 2026-10-28: `adsl-lstalvdt-amb` spec reworded to match the oracle

- The spec said "any dated record ... (`ae`, `lb`, `vs` and the treatment end date)", which read as if vital signs count, while the oracle (the clear twin's reading) ignores `vs`. the spec was reworded the spec rather than switch the oracle. New wording lists the provided datasets without saying which count, so the task is still ambiguous but no longer contradicts the oracle. `with-vs` stays a stored defensible reading.
- Effect on results: runs on this task before 2026-10-28 (K2b, E8 v3 and v4, p1a not affected) saw the old wording; the benchmark is not frozen, and those cells are not rerun. Treat their `adsl-lstalvdt-amb` counts as old-spec results.

## 2026-10-28: E8b results: a local reviewer of assumptions lists does not discriminate

- `results/e8b/summary.md`. qwen3-coder:30b as reviewer asked on 17% of ambiguous and 23% of clear samples; gpt-oss:20b on 98% and 73%. H1 supported only with gpt-oss (which asks on nearly everything), H2 not supported, H3 split (gpt-oss named the first-dose-day boundary in 8 of 9 `adae-trtemfl-amb` reviews, qwen in 1 of 9).
- Decision: do not build the assumptions check into the harness as a single-prompt local reviewer. The Claude reviewer run (about $0.03) was skipped because no local reviewer showed discrimination, as pre-registered; it remains the cheapest next test, with a reviewer that names competing readings and whether each changes the output.

## 2026-10-28: E8b (assumptions review) design, fixed before any run

- **Question:** can a separate reviewer call, shown only the spec and the programmer's `ASSUMPTIONS:` list (no code, no oracle, no ambiguity notes), decide what to escalate better than the programmer's own ask? E8 showed the lists name the open point even when the programmer proceeds silently.
- **Data:** the logged `k2-v4` assumption lists from E8 (`results/e8/<model>/v4/scores.jsonl`: Haiku 5.5, Sonnet 5.5, qwen3-coder:30b; 11 k2b tasks, 5 ambiguous and 6 clear, 3 samples). Only samples where the programmer wrote an assumptions list are reviewed (a programmer escalation already is an ask). No new programmer runs.
- **Reviewers:** qwen3-coder:30b and gpt-oss:20b (local, free), then Claude Haiku 5.5 only if a local reviewer shows signal (about $0.03 expected). One reviewer prompt, written once (`tare/prompts.py`, `REVIEWER_PROMPT`): reply `ESCALATE: <question naming the choice>` if a listed assumption is a choice the spec does not settle and that would change the output, otherwise `PROCEED`; do not escalate on choices the spec states or on harmless defaults. Temperature 0.2 for local reviewers. The prompt is not tuned on these results; if it must change, the change and the reason are logged and all cells rerun.
- **Metrics:** per (programmer model, reviewer): ask rate on ambiguous samples, false-escalation rate on clear samples, and for the pipeline (programmer asks OR reviewer asks) the same two rates. Question quality on `adae-trtemfl-amb` and `adlb-ablfl-amb` (the open points that move the oracle's answer) checked by hand against the ambiguity note.
- **Hypotheses:** H1: the pipeline ask rate on ambiguous samples exceeds the programmer's own v4 ask rate for every programmer model (Haiku 4/15, Sonnet 0/15, qwen 0/15). H2: false escalation on clear samples stays at or below 25% (Haiku v3 alone had 8/18). H3: on `adae-trtemfl-amb` and `adlb-ablfl-amb` the reviewer's questions name the first-dose-day boundary in at least half of the reviewed samples that list it.
- **Limits stated in advance:** 33 samples per programmer model, correlated; 5 ambiguous tasks, labels by one author; the reviewer sees assumptions that are tied to specific samples. A reviewer that escalates on everything would pass H1 and fail H2.

## 2026-10-27: Defensible readings stored for the 11 ambiguous tasks

- Scoring rule from the go/no-go implemented: a silent error equal to a stored alternative reading keeps the class `silent_error` and gets `matches_reading` set; the oracle stays the single scored answer.
- 15 alternatives kept. Ten more candidates produced output identical to the oracle on this data and were dropped: a missing last dose date (TRTEMFL, ONTRTFL), tie order by LBSEQ (ABLFL), partial and missing-dose exposure records (SAFFL, TRTSDT), complete-dates-only (LSTALVDT), no first-dose adjustment (ASTDT), and a CHG variant equal to another. Several open points named in `ambiguity_note` therefore cannot change the output on this dataset; a model can still be asked about them, but divergence there is not measurable until perturbed inputs exercise them.
- `adsl-lstalvdt-amb`: the spec lists `vs`, the oracle ignores it; see the open question in STATUS.

## 2026-10-27: E8 results: prompting raises asking unevenly and with false alarms; assumptions lists surface the open point
- **Results** (`results/e8/summary.md`): ask rate on the 15 ambiguous samples, Haiku 0 (baseline) to 9 (v3) to 4 (v4); Sonnet 0 to 1 to 0; qwen3-coder:30b 0 to 3 to 0. False escalations on the 18 clear samples: Haiku 8 (v3), 2 (v4); Sonnet 2, 1; the 30B 0 (v3), 7 (v4).
- **Hypotheses:** H1 supported (strongly for Haiku only); H2 not supported (the checklist plus assumptions asked less than the stronger instruction alone); H3 not supported (Haiku v3 and the 30B v4 raised many false escalations, though Haiku's mostly asked about real residual gaps that do not occur in this data).
- **Key observations:** the ambiguity that shifts the oracle's answer (strict versus inclusive first-dose boundary) was never asked about by any model; under v4 all 6 non-escalated Claude samples on `adae-trtemfl-amb` wrote the exact open point in their assumptions and proceeded anyway. This supports building an assumptions check into the harness (decided 2026-10-27), but whether an automated reviewer can separate consequential from harmless assumptions is untested.
- **Cost:** $0.9532, within the $2 confirmation line; logged in the spend table.

## 2026-10-27: E8 (escalation elicitation) design, fixed before any run
- **Question (RQ1b):** can prompting make models ask when a spec is ambiguous, without false alarms on clear specs? Baseline already measured under prompt `k2-v2` (optional `ESCALATE:` reply): 0 escalations in 165 samples (five models, harder round).
- **Variants (prompt text is in `tare/prompts.py`, committed with this entry):** `k2-v3` a stronger instruction (check for readings that change the output; silently guessing is the failure; do not ask about things the spec settles); `k2-v4` v3 plus a checklist of common ambiguities (date boundaries, which records count, ties and ordering, partial dates and missing values, inclusive counts, date versus datetime) and a required `ASSUMPTIONS:` list before the code or the question.
- **Setup:** the 11 harder-round tasks (5 ambiguous, 6 clear), 3 samples, up to 2 repairs, Claude Haiku 5.5, Claude Sonnet 5.5 and qwen3-coder:30b. Estimated API cost about $0.6-1.1 for the four Claude runs, under the $2 line.
- **Measures:** ask rate on the 15 ambiguous samples per run; false-escalation rate on the 18 clear samples per run; class counts; the questions asked and the assumptions listed (read by hand). Whether an assumption "names the open point" is my own judgment and will be reported with quotes, not as an automatic metric.
- **Hypotheses:** H1 the stronger instruction raises the ask rate above 0 for at least one model; H2 the checklist and assumptions list raise it further; H3 false escalations on clear tasks stay low. Any of these may fail; every result will be reported.
- **Caveat on the checklist:** its items overlap the kinds of ambiguity in these five tasks, so v4 shows what a checklist can do on known ambiguity classes, not that models detect unknown ones. The small task set and the subjective reading of assumptions are further limits.

## 2026-10-27: Go/no-go decided: GO WITH CHANGES; reposition around silently resolved ambiguity
- **Decision:** The draft recommendation in `docs/STATUS.md` was approved ("go with changes").
- **Why:** K2 failed as written (frontier models made 0 silent errors on 20 explicit seed tasks and none on the explicit harder-round tasks), but on deliberately ambiguous specs every model silently chose a reading and none ever asked (0 of 165 harder-round samples), and models from different families often chose the same reading (Claude pair identical in 8 of 9 both-wrong samples; `gpt-oss:20b` identical to both Claude models on 2 ambiguous tasks; `gpt-oss:20b` and `qwen3-coder:30b` byte-identical on an explicit-spec bug). Output comparison alone cannot catch a choice every programmer makes the same way. Details: `results/k2b/summary.md`, `results/k2_local/summary.md`.
- **What changes:** headline and research questions (`docs/01_PROJECT_BRIEF.md`: new RQ1b); ambiguity as a first-class benchmark axis, about 30% of tasks with clear twins (`docs/04_BENCHMARK_SPEC.md`); escalation-elicitation experiment E8 and new metrics (`docs/05_EXPERIMENTS.md`); Phase 1 and 2 re-scoped (`docs/08_ROADMAP.md`); README updated.
- **Not changed:** the hard rules, the $40 API cap, the isolation and sandbox design, the oracle approach, Phase 3 stays optional.
- **Would change if:** an external rating shows that the "ambiguous" tasks are not ambiguous to clinical programmers, or elicitation prompts raise the ask rate to near the clear-twin rate cheaply (the premise would then weaken to "models ask when prompted").

## 2026-10-27: gpt-oss:20b original-round run covered all 31 tasks; configs now pinned to a round
- The original-round gpt-oss config had no `round` filter, so after the harder round existed it ran all 31 tasks (93 samples) instead of 60, the extra 33 under the no-escalation prompt. Result: no harm (records split by round; the extra part became a prompt comparison), but about 80 minutes of extra run time. All original-round and harder-round configs now set `round`.
- Results: `results/k2_local/summary.md` (addendum) and `results/k2b/summary.md`.

## 2026-10-26: Harder round K2b: tasks fixed before any model ran (pre-registration)
- **Why:** K2 failed (frontier models 20/20); the roadmap's response is harder derivations before repositioning. \"Harder round\" was chosen on 2026-10-26.
- **What (11 tasks, round `k2b`, all `dev`):** four explicit hard derivations from the standard oracle (`adlb-ontrtfl-std`, `adae-aoccifl-std`, `adae-lastdose-std` with `LDOSEDTM` and `DOSEON`, `adlb-maxrec-std` derived-record rows); two perturbed-input tasks on a seeded same-day-repeat lab file (`adlb-ablfl-sameday`, `adlb-lvotfl-sameday`; `r/perturb.R`, oracle `pert-sameday-lb`, 6,621 repeat records added); five deliberately ambiguous tasks (`*-amb`) with terse specs and the standard oracle as the interpretation (`adsl-trtdurd-amb`, `adsl-saffl-amb`, `adae-trtemfl-amb`, `adlb-ablfl-amb`, `adsl-lstalvdt-amb`).
- **Checks before running:** independent reference solutions match the oracle on all 11 (and on the original 20); how much each alternative reading changes the answer on the ambiguous tasks: TRTDURD inclusive vs elapsed 252/306 subjects; SAFFL "active dose only" 86/306; TRTEMFL "strictly after first dose" 28/1191; ABLFL strictly before 24 records; LSTALVDT with vital signs 45/306. (The missing-last-dose-date question in `adae-trtemfl-amb` changes nothing in this data.)
- **Prompt k2-v2** adds an option: reply `ESCALATE: <question>` and no code. Escalation is its own outcome (`escalated`): good on `*-amb` tasks, a false escalation on the others. The 20 original tasks were run under k2-v1 (no escalation option).
- **No tuning:** every model result on these tasks will be reported, whatever it shows; no task will be changed or dropped because of how models did on it (a task found to be wrong or unfair would be reported and replaced by a new version, not quietly edited). The round was designed to be harder, so it is not a random sample of real work.
- **Scorer fix found while verifying:** tz-aware oracle timestamps (R POSIXct) were compared as unequal to plain dates; fixed in `tare/compare.py`, with a test.
- **Design learning:** the admiral ADLB template requires a unique (subject, parameter, date, visit) key, so a same-day repeat has to be modeled as an unscheduled visit with its own visit number; a repeat of an exact zero value would tie on value and make the answer depend on row order, so repeats of zero get a distinct non-zero value.

## 2026-10-26: K2 failed its pass line: frontier models make no silent errors on the 20 seed tasks
- **Result:** Haiku 5.5 and Sonnet 5.5 both 20/20 correct (Sonnet needed one repair); pass line was at least 3 of 20. Spend $0.2431. Details: `results/k2_frontier/summary.md`.
- **Reading:** consistent with the "Positioning after the audit" entry's own caveat (frontier models are near-perfect on the clean pilot data). Tare's seed tasks are explicit and well specified, which probably favors the models; real specs are vaguer.
- **Roadmap response (needs approval, since it affects scope):** build a harder round (visit windowing, LOCF derived records, baselines with unscheduled visits, partial-date variants, deliberately ambiguous specs) and rerun; only if those also give near-zero silent errors, reposition around local and firewall correctness plus cost, where the measured error rates are not near zero (qwen3-coder:30b 85% correct, qwen2.5-coder:7b 42%).
- **Logging fix:** call logs now record `stop_reason` and the parameters actually sent (a silent replace had skipped both; the Haiku run's call log lacks `stop_reason`; its config params matched what was sent).

## 2026-10-18: Anthropic client built; Claude model IDs and prices verified
- **Verified** on Anthropic's live docs: `claude-sonnet-5-5` $2/$10 and `claude-haiku-5-5` $0.10/$0.50 per million tokens (up to 100k-token prompts). The cached table inside the bundled API skill was stale (it listed Haiku 4.5 as the cheap model); the live pricing and models pages are the source of truth. `05_EXPERIMENTS.md` was right.
- **No sampling parameters on API runs** (Claude 5.5 models reject non-default values), so API and local runs differ in temperature; recorded in the config and manifest. **No refusal fallbacks**, so each result belongs to the model named in the config.
- **Cost tracking:** `configs/pricing.yaml`, `tare/pricing.py`; every sample record carries `cost_usd` and every run summary a total.
- **Cost estimate before the first paid run (not yet run):** expected about $0.7-1.8 for Sonnet 5.5 and $0.03-0.10 for Haiku 5.5, driven mostly by adaptive-thinking output tokens, which I can't know in advance; a bad case could pass $2. Plan: run Haiku 5.5 first (under $0.15 even if it goes badly), measure real tokens per task, project Sonnet from that, and ask before the Sonnet run if the projection exceeds $2.

## 2026-10-17: qwen3-coder:30b pulled; local K2 arm run
- 18 GB pull, approved; the download was slow (about 0.3 MB/s at first), so Ollama resumed it across several background runs. Local arm result and the first K3 numbers: `results/k2_local/summary.md`.

## 2026-10-12: K2 kit built: 20 tasks, scorer and reference solutions
- **What:** 10 standard and 10 sponsor-variant tasks (`benchmark/tasks/`, specs in `benchmark/specs/`), all `dev` split. Variants are real patches to the admiral templates (`r/variants/variants.R`), each with its own oracle run (`r/oracle_build.R`, outputs in git-ignored `data/oracle/`). Answer keys live in `data/answers/`, separate from the bundles a programmer sees (`data/tasks/`).
- **Well-posedness check:** I wrote an independent Python reference solution per task (`benchmark/reference/`) from the spec text; all 20 score `correct` against the oracle (`scripts/run_references.py`). Running each standard reference on its variant task scores `silent_error` with mismatch counts equal to the standard-versus-variant oracle difference. Limitation: the references and specs were written by the same author (Claude), so this is not an independent human ambiguity review.
- **Variant changes after checking the data:** an `AGEGR1` variant with a 65 cut point would equal the standard answer (every subject is 50-89), so the variant uses 65 and 75. An `LSTALVDT` "ignore partial dates" variant changed 0 of 306 subjects, so it became "also count vital-sign dates" (45 of 306 differ). Lab tasks use all original (non-derived) lab records, because on a 4-parameter subset the strict-baseline variant changed nothing; derived `DTYPE` rows are excluded because they reuse `LBSEQ`.
- **Contract choices:** the contract checks structure, types, nulls and flag domains (Y/N) but not category labels (`AGEGR1`, `EOSSTT`), so a model that ignores a variant's labels is a silent error, not a loud one. Extra output columns are ignored. Empty string counts as null for strings; date and timestamp are accepted for date columns; numbers use tolerance 1e-8 x max(1, |x|). This relaxes one line of `04_BENCHMARK_SPEC.md` ("extra columns" are not a violation).
- **Scorer:** `tare/compare.py` and `tare/score.py` (shared with the future comparator), with unit tests. Sandbox runs go through `tare/isolation.py` (allowlist plus forbidden paths, tested with attempted leaks).
- **K2 cost estimate (API):** about 25k prompt tokens for the 20 tasks in total; at the unverified list prices in `05_EXPERIMENTS.md` ($2/$10 and $0.10/$0.50 per million tokens), one attempt per task costs about $0.23 for Sonnet 5.5 and $0.01 for Haiku 5.5, with a worst case of three attempts per task of about $0.69 and $0.04. Well under the $2 confirmation line, but the prices still need VERIFY.

## 2026-10-12: K1 passed; the oracle reference is Tare's own pinned regeneration, not `pharmaverseadam`
- **Why:** K1a (shipped templates vs `pharmaverseadam`): ADSL 0 of 55 variables differ, ADLB 0 of 115, ADAE 3 of 107 (`LDOSEDTM`, `DOSEON`, `DOSEU`; the installed template counts a same-day dose as the last dose, the packaged data doesn't; cause in the package build not verified). K1b (shift all SDTM `--DTC` +4 years): 0 mismatches against the shifted baseline in all three datasets, with an unshifted control that does differ. Details: `results/k1/summary.md`.
- **Also:** ADAE and ADLB templates read `admiral::admiral_adsl`, so the oracle chains our regenerated ADSL into them. Each template runs in a fresh `Rscript` process with its data reads shimmed and its cache write removed (`r/run_template.R`).
- **Would change if:** a later template variant or perturbation breaks the metamorphic relation without an explanation.

## 2026-10-12: Setup decisions and doc fixes (first session)
- **Repo root is `Tare/`** (docs moved up out of `tare-docs/`). GitHub repo `tare`, private until Phase 1 results exist. The name is free under `thetanishrana`.
- **PyPI:** `tare` is taken (an unrelated project). The distribution name is **`tare-qc`** (free); the import package and CLI stay `tare`.
- **Model totals:** ~38 GB for the three core models, ~52 GB with optional devstral:24b (the earlier "38 GB in total" left devstral out).
- **Docker Desktop VM capped at 4 GB** so it doesn't compete with the local model for 32 GB. Per-run sandbox limit stays 2 GB.
- **R upgraded 4.3.2 to 4.6.1** (current CRAN release): CRAN only ships macOS binaries for current and recent R, so 4.3.2 would have meant compiling from source. renv pins the 4.6 series; snapshot type `all`.
- **Ollama is started by `scripts/ollama_serve.sh`**, not `brew services`, because the brew plist can't take `OLLAMA_CONTEXT_LENGTH` (16384) and may be overwritten on upgrade.
- **Kickoff prompt** in `00_START_HERE.md` now includes `STATUS.md`.
- **K2 uses the API** (key in `.env`, monthly spend limit set in the Console). Estimate the cost first; confirm if over $2.
- **Verified:** `rocker/r-ver` and `rocker/tidyverse` have arm64 manifests; `qwen2.5-coder:7b` tag valid (4.7 GB).
- **Still VERIFY:** who can get a CDISC Library API key.

## 2026-10-12: CLAUDE.md stays short; detail lives in `docs/`
- **Why:** an ICLR 2026 study found that repository context files (AGENTS.md, CLAUDE.md) often reduced coding-agent success and raised cost by about 20%, and recommended minimal requirements. Detail is loaded on demand from `docs/`.

## 2026-10-12: Project name Tare (repo, package and command: `tare`)
- **Why:** to tare a scale is to zero it before weighing, so the reading you get is true. The project makes AI-written clinical code trustworthy before anyone relies on it. Short and understated, no puns. A quick search found no AI or pharma tools with the name.
- **Rejected earlier:** "Crossbearing" (religious connotation), "Eve" and "Janus" (religious or mythological), "Corroborate" and other agreement metaphors (too literal), "clinqc" (felt cheesy), "ADaM-Bench" (easily confused with the Adam optimizer).
- Checked 2026-10-12: PyPI `tare` is taken, `tare-qc` is free, GitHub `tare` is free. Short dictionary words are often taken on PyPI. If it's taken, publish the package under a variant such as `tare-qc` and keep Tare as the project name.

## 2026-10-12: Local models are core, not optional
- **Why:** they run the trained model; they make the behind-the-firewall configuration possible; they give a free second model family (gpt-oss for OpenAI, Qwen, Mistral); they make enough errors to measure catch rates (frontier models are about 97–100% accurate on the clean pilot data per Merck); and development calls are unlimited and free.
- **Runtime:** Ollama for serving (easy model management). MLX for training. Serving through MLX is an acceptable alternative if it simplifies things.

## 2026-10-12: Paid API only for final, reported runs
- **Why:** reproducibility (pinned model versions, logged tokens), and Anthropic's terms (products built with the Agent SDK should use API keys; subscription OAuth is for ordinary use of Claude Code and Anthropic's apps). Subscriptions are used to *build* the project with Claude Code and Codex, never as the harness's model backend.
- **Budget:** $40 hard cap. Expected about $10–25 for the final Claude runs.
- **Cost reporting:** API-equivalent cost computed from token counts × list prices, so local runs can be compared without spending.

## 2026-10-12: Positioning after the audit: "the rigorous test of whether AI QC catches AI errors"
- **Why:** Merck (PharmaSUG 2026 AI-201) already used an isolated Claude instance as an AI QC programmer on the CDISC pilot data. Tare builds on it and addresses its stated limitations: one model family, possible correlated errors, one clean benchmark, and a leak where the QC program read the production ADSL output.
- **Would change if:** K2 shows almost no silent errors. Then reposition around local and firewall correctness plus cost.

## 2026-10-12: Same-family checking is a control, not the method
- **Why:** an ICML 2025 study of over 350 LLMs found that when two models are both wrong, they agree about 60% of the time, and larger models are more correlated. Programmers A and B come from different families and, where possible, different languages (R and Python).

## 2026-10-12: Memorization controls are mandatory
- **Why:** the admiral templates and CDISC pilot data are public, so models may reproduce answers from memory. Controls: sponsor variants, perturbed inputs, held-out therapeutic areas, specs in our own words, and separate reporting for standard and controlled tasks.

## 2026-10-12: CDISC CORE is optional, not core scope
- **Why:** it needs a CDISC Library API key (eligibility unclear) and a rules cache kept in sync with the package version, and it checks conformance, not value correctness.

## 2026-10-12: Domain is clinical trial statistical programming (ADaM derivation QC)
- **Why:** a real, expensive problem (12–24 FTE-months of programming per Phase 3 study); free public data (the pharmaverse packages, Apache-2.0); an oracle that can generate new exact answers (admiral templates); and a trust process the industry already uses (double programming).
- **Alternatives considered and rejected:** pharmacovigilance case processing (data is private, vendors are already shipping); SDTM mapping with CORE validation (already presented at PharmaSUG 2026); harmony writing for music (not corporate); energy-market agents, health-records agents, CAD, infrastructure code, C-to-Rust and Rust verification (crowded or already benchmarked).

## 2026-10-12: Constraints
- Minimal spending. No long waits: the duration should come from the work itself. Corporate domain preferred.

## Open questions
- Are the original CDISC pilot ADaM datasets and define.xml publicly available with a usable license? They'd give a second answer key and realistic spec text.
- Who can get a CDISC Library API key? Only matters for optional CORE checks.
