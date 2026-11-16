# Project brief

## In one line

**Tare: independent AI double programming for clinical trial datasets, and a measurement of when it fails.**

The name: to tare a scale is to zero it before weighing, so the reading you get is true. Tare does that for AI-written clinical code.

## The 30-second version

Pharma companies turn raw trial data into standardized analysis datasets (CDISC ADaM). Every efficacy and safety table submitted to regulators is built from them. AI coding tools now draft much of this code, and the dangerous failure isn't code that crashes. It's code that runs cleanly and quietly produces a wrong value, such as one patient wrongly counted in a safety population. The industry's standard safeguard is double programming: two programmers implement the same spec independently and compare outputs. Tare measures how often AI-written clinical code is silently wrong, and builds a harness where independent AI programmers from different model families, isolated from each other, catch each other's errors. It measures when that works and when correlated errors slip through.

**Direction after the first experiments (approved 2026-10-27).** On explicit, well-written specs, frontier models made no silent errors in our tests (Claude Haiku 5.5 and Sonnet 5.5: 20 of 20 seed tasks and 18 of 18 harder-round clear-task samples each correct). The silent errors appeared where specs were ambiguous: every model tested silently picked a reading and **none ever asked a question** (0 escalations in 165 harder-round samples across five models), and models, including ones from different families, often picked the same reading, so agreement between them did not mean the answer was the intended one (`results/k2b/summary.md`). Tare's headline is therefore about silently resolved ambiguity and what catches it, not about frontier models getting explicit derivations wrong.

## Why this problem

- **It's expensive.** Statistical programming for a typical Phase 3 study takes an estimated 12–24 FTE-months and produces 100–500 tables, listings and figures across 8–15 ADaM datasets (ClinAgent paper).
- **Code that runs isn't code that's right.** A pharma training course demonstrates AI-drafted code that runs cleanly but silently corrupts a safety-population count, then shows the independent QC check that catches it (Datanovia). A 2026 industry paper states it plainly: successful execution doesn't by itself guarantee a correct derived variable (Yesod AI, PharmaSUG 2026 AI-431).
- **The industry already trusts double programming.** It's the long-standing gold standard for QC, though not a regulatory requirement (PharmaSUG 2025 MM-227). Fitting AI into that existing trust process is more credible than asking reviewers to trust a model.
- **Many companies can't send trial data to outside APIs.** That's why a local, behind-the-firewall configuration matters.

## Prior work, and where Tare differs

| Work | What it did | What it left open |
|---|---|---|
| **Merck, PharmaSUG 2026 AI-201** (closest) | A separate, isolated Claude instance wrote QC programs from specs, compared record by record against validated ADaM data from the public CDISC pilot study. Mean match 97.1–100% per dataset. 43 of 54 variables matched perfectly. Lowest: ADSL WEIGHTBL 93.7%, ADADAS AVISITN 90.9%. ADAE TRTEMFL differed on 6 records. | One model family, so the authors flag correlated errors as a limitation. One clean benchmark. Their code review found the QC program had read the production ADSL output to infer a pooling rule, which is a leak that breaks independence. |
| **ClinAgent** (medRxiv 2026) | MCP tools and skills that give coding agents clinical programming abilities. Spec derivation accuracy 72.1% (251/348 variables). | Didn't measure silent errors or test double programming. One synthetic study. |
| **Yesod AI, AI-431** | Multi-agent ADaM pipeline with execution sandbox and automated QC checks. | Reports only time savings, no accuracy. |
| **Takeda, AI-125** | Claude via Bedrock validates ADaM specs and generates SAS code. | No accuracy metrics. |
| **Merck, AI-332** | AI-assisted conversion of external ADaM programs to sponsor standards. | Time estimates only. |
| **Merck, AP-211** | TLF templates and R code with iterative debugging. | "Success" means the code runs and its output has a plausible shape, not that values are correct. |
| **PharmaSUG 2026 SS-261** | AI SDTM mapping with automated CDISC CORE conformance checks in a loop. | Different stage (SDTM mapping). Checks conformance, not value correctness. |
| **Correlated Errors in LLMs** (ICML 2025) | Over 350 models: when two models are both wrong, they give the same answer about 60% of the time, and larger, more accurate models are more correlated. | Not about clinical code, but it predicts AI double programming may be weaker than it looks. |

**What Tare adds:**
1. **A silent-error benchmark** for ADaM derivations, with controls against memorization (sponsor-specific spec variants, perturbed inputs, held-out therapeutic areas) and an **ambiguity axis**: deliberately underspecified specs, each with a matched clear twin, scored on whether the model asks or silently chooses.
2. **Cross-family, cross-language double programming** with structural isolation: programmers can't read production outputs or each other's code, by construction.
3. **Measured error correlation** between models, which tells you when double programming fails.
4. **Cost-matched baselines.** Double programming spends at least twice the tokens, so it has to beat single-programmer setups with the same budget.
5. **A local configuration** and a small trained model for teams that can't use external APIs.

## Research questions

- **RQ1:** How often do frontier and local models produce *silent* errors on ADaM derivations, which kinds of derivation cause them, and how much of that is silent resolution of an ambiguous spec versus a coding mistake on a clear one? (Early answer: for frontier models, almost entirely the former.)
- **RQ1b:** When a spec is ambiguous, do models ask, and can prompting, structure or an adjudicator raise the ask rate without false alarms on clear specs? (Baseline: 0 of 165 samples asked. First E8 answer: a stronger prompt gets Haiku to ask on 9 of 15 ambiguous samples but with 8 false alarms in 18 clear ones, and barely moves Sonnet; assumptions lists expose the open point even when the model does not ask. `results/e8/summary.md`.)
- **RQ2:** How correlated are errors across model families? Within one family?
- **RQ3:** Does cross-family double programming with adjudication reduce escaped errors more than cost-matched single-model alternatives?
- **RQ4:** How often does the harness need a human, and are its escalation questions useful?
- **RQ5 (stretch):** Can a small local model trained against the execution checker (and an ambiguity-aware reward) be a useful independent programmer, for example one that learns to escalate?

## Audience

- **Engineers:** a hard problem, a clean benchmark with controls, an oracle for generating data, isolation by construction, statistics with confidence intervals.
- **Pharma and clinical programmers:** respect for how QC actually works, correct terminology, no overclaiming.

## Success criteria

- **Minimum (Phases 1–2):** a frozen benchmark of about 150 tasks including a substantial ambiguous subset with clear twins; silent-error and escalation rates for at least 4 models; harness results with cost-matched baselines and an error-correlation analysis; public repo, write-up and short demo.
- **Stretch (Phase 3):** a 1.7–4B local model that is better on the benchmark after training, measured in the harness as programmer B.

## Non-goals

- Not a submission tool and not validated software.
- Not SDTM mapping, TLF generation or define.xml generation. Possible later, out of scope now.
- No proprietary or patient-identifiable data, only public and synthetic.
- CDISC CORE conformance checks are optional extras, not core scope. They need a CDISC Library API key.

## Honest framing (use these lines)

- "Research prototype on public CDISC pilot data, not validated for regulatory use."
- "Builds on Merck's PharmaSUG 2026 study of AI-generated QC code. It adds cross-family independence, memorization controls and error-correlation measurement."
