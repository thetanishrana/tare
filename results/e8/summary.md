# E8: can prompting make models ask when a spec is ambiguous?

Run 2026-10-27. Design fixed and committed before any run (`docs/09_DECISIONS.md`, entry "E8 design"). The 11 harder-round tasks (5 ambiguous, 6 clear), 3 samples per task, up to 2 repairs, Claude Haiku 5.5, Claude Sonnet 5.5 and qwen3-coder:30b, under three prompts: `k2-v2` (baseline: an optional `ESCALATE:` reply, from `results/k2b/`), `k2-v3` (a stronger instruction) and `k2-v4` (v3 plus a checklist of common ambiguities and a required `ASSUMPTIONS:` list). Prompt text is in `tare/prompts.py`. Score records (with the questions asked and the assumptions listed), manifests and configs: `<model>/<prompt>/` here. API cost: $0.9532 (Haiku $0.0264 + $0.0415, Sonnet $0.4056 + $0.4797).

## Results (out of 15 ambiguous-task samples and 18 clear-task samples per cell)

| model | prompt | asked on ambiguous | asked on clear (false escalation) | ambiguous outcomes (S silent error, C correct, E escalated) |
|---|---|---|---|---|
| Haiku 5.5 | v2 baseline | 0/15 | 0/18 | S9 C6 |
| Haiku 5.5 | v3 stronger instruction | **9/15** | **8/18** | S3 C3 E9 |
| Haiku 5.5 | v4 checklist + assumptions | 4/15 | 2/18 | S6 C5 E4 |
| Sonnet 5.5 | v2 baseline | 0/15 | 0/18 | S9 C6 |
| Sonnet 5.5 | v3 | 1/15 | 2/18 | S9 C5 E1 |
| Sonnet 5.5 | v4 | 0/15 | 1/18 | S9 C6 |
| qwen3-coder:30b | v2 baseline | 0/15 | 0/18 | S12 C3 |
| qwen3-coder:30b | v3 | 3/15 | 0/18 | S9 C3 E3 |
| qwen3-coder:30b | v4 | 0/15 | 7/18 | S8 C7 |

## Against the pre-registered hypotheses
- **H1 (stronger instruction raises the ask rate above 0 for at least one model): supported**, strongly for Haiku (0 to 9 of 15), weakly for the 30B (3 of 15) and barely for Sonnet (1 of 15).
- **H2 (checklist plus assumptions raise it further): not supported.** v4 asked less than v3 for every model (Haiku 4 vs 9, Sonnet 0 vs 1, 30B 0 vs 3).
- **H3 (false escalations stay low): not supported for Haiku v3 (8 of 18) and for the 30B under v4 (7 of 18).** Context: Haiku's false escalations asked about real residual gaps, such as a final tie-break the spec does not define, which never occurs in this data (no full ties exist). The 30B's v4 "questions" were mostly "Should I assume ...?" restatements of defaults.

## What the questions show
- **Asking is not the same as asking the right thing.** On `adsl-trtdurd-amb` Haiku asked exactly the open point (inclusive or elapsed) in all 3 v3 samples. On `adlb-ablfl-amb` Haiku and the 30B asked about same-day tie-breaking or missing values and **never about whether the first dose day counts**, the point that moves the oracle's answer. On `adsl-lstalvdt-amb` Haiku asked which AE date columns count, not whether vital signs count. On `adae-trtemfl-amb` **no model asked in any run**: 0 escalations in 27 samples (3 models x baseline, v3 and v4 x 3 samples; checked from the records).
- **The assumptions list surfaces what escalation does not.** Under v4 every non-escalated Claude sample on `adae-trtemfl-amb` (6 of 6) wrote the exact open point down, for example "starts after the first dose is read literally as strict ... an AE starting on the first-dose date is not flagged" (Haiku, one sample added that many CDISC implementations use `>=` and that the choice changes the output), and then proceeded silently. Sonnet wrote "Before TRTSDT is strict ... a result on the first-dose date is not baseline" in 3 of 3 v4 samples on `adlb-ablfl-amb` while also never asking. A regex heuristic over the assumptions text (named the relevant point) gives 3 of 3 for both Claude models on `adae-trtemfl-amb`; for the 30B it is 2 of 3 on that task and 0 of 3 on `adlb-ablfl-amb`. The regexes are loose and only the quoted Claude cases were checked by hand: treat these counts as indicative.

## Conclusions, with limits
1. **Prompting alone moves the ask rate very unevenly across models** (Haiku a lot, Sonnet almost not at all) and does so at the price of false alarms; there is no setting here that asks on ambiguous tasks and stays quiet on clear ones.
2. **The ambiguity that shifts the oracle's answer is exactly the one models ask about least.** All models silently read "after the first dose" as strict.
3. **A required assumptions list makes the unflagged choice visible**, so a reviewer, adjudicator or second model could catch it even when the programmer will not ask. This supports the harness design change (an assumptions check) approved on 2026-10-27, but whether an automated reviewer can reliably tell consequential assumptions from harmless ones is untested.
4. Limits: 11 tasks, 5 of them ambiguous; 3 samples per cell, not independent; one prompt wording per variant; the checklist overlaps the ambiguity classes in these tasks; no external rating of whether the tasks are ambiguous to clinical programmers.
