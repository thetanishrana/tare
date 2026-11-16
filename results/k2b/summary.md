# K2b: the harder round (11 tasks): Claude Haiku 5.5, Claude Sonnet 5.5, gpt-oss:20b, qwen3-coder:30b, qwen2.5-coder:7b

Run 2026-10-26. 11 new tasks (round `k2b`: 4 explicit hard, 2 perturbed same-day inputs, 5 deliberately ambiguous), 3 samples per task per model, prompt `k2-v2` (the model may reply `ESCALATE: <question>` instead of writing code), up to 2 repairs for loud errors. The task list was committed before any model ran (`docs/09_DECISIONS.md`, 2026-10-26), and every result is reported below, including the ones that look bad for the benchmark. Score records, manifests and configs are copied into `haiku55/`, `sonnet55/`, `qwen3coder30b/`, `qwen25coder7b/` and `gptoss20b/` here. The original 20 seed tasks are also being run on `gpt-oss:20b`; that result will be added to `results/k2_local/summary.md`.

Frontier settings: no sampling parameters sent (Claude 5.5 models reject non-default values), adaptive thinking at each model's default effort, no refusal fallbacks. Local settings: temperature 0.2; 4096 max tokens (8192 for `gpt-oss:20b`, a reasoning model). API cost for this round: Haiku $0.0350, Sonnet $0.3556.

## Results

| Model | clear tasks (6 tasks, 18 samples) | ambiguous tasks (5 tasks, 15 samples) | escalations |
|---|---|---|---|
| Claude Haiku 5.5 | 18 correct | 6 correct, 9 silent errors | 0 of 33 |
| Claude Sonnet 5.5 | 18 correct | 6 correct, 9 silent errors | 0 of 33 |
| gpt-oss:20b | 17 correct, 1 loud | 6 correct, 9 silent errors | 0 of 33 |
| qwen3-coder:30b | 13 correct, 3 silent, 2 loud | 3 correct, 12 silent errors | 0 of 33 |
| qwen2.5-coder:7b | 8 correct, 1 silent, 9 loud | 3 correct, 7 silent, 5 loud | 0 of 33 |

Classes are final outcomes after repairs. Per task (C correct, S silent error, L loud error; samples 0-2):

| task | ambiguous | Qwen 7B | Qwen 30B | gpt-oss 20B | Haiku | Sonnet |
|---|---|---|---|---|---|---|
| adae-aoccifl-std | | L L L | S S C | C C C | C C C | C C C |
| adae-lastdose-std | | L L L | C C L | C C L | C C C | C C C |
| adlb-maxrec-std | | C C C | C C S | C C C | C C C | C C C |
| adlb-ontrtfl-std | | C C C | C C C | C C C | C C C | C C C |
| adlb-ablfl-sameday | | S C L | L C C | C C C | C C C | C C C |
| adlb-lvotfl-sameday | | C L L | C C C | C C C | C C C | C C C |
| adae-trtemfl-amb | yes | S S L | S S S | S S S | S S S | S S S |
| adlb-ablfl-amb | yes | S L S | S S S | S S S | S S S | S S S |
| adsl-lstalvdt-amb | yes | L L L | S S S | S S S | S S S | S S S |
| adsl-saffl-amb | yes | C C C | C C C | C C C | C C C | C C C |
| adsl-trtdurd-amb | yes | S S S | S S S | C C C | C C C | C C C |

## What it shows

1. **Explicit specs, even hard ones, give the frontier models and `gpt-oss:20b` almost no errors** (Haiku 18 of 18, Sonnet 18 of 18, gpt-oss 17 of 18 correct; its one failure was a loud error where it wrote an integer into a date column). The two Qwen models do fail on explicit specs: the 30B with silent errors on `adae-aoccifl-std` (2 of 3 samples, 882 of 1,191 records wrong) and `adlb-maxrec-std` (1 of 3, 4,512 of 7,481 rows wrong); the 7B mostly produced no usable output (9 of 18 clear-task samples loud, 1 silent).
2. **On ambiguous specs, every model silently resolves the ambiguity and none escalates**: 0 escalations in 165 samples across the five models, and no false escalations on the clear tasks either. On three of the five ambiguous tasks the models that produced output made the same silent choice: strict "after" for the first dose day in `adae-trtemfl-amb` (28 AEs differ from the oracle), strict "before" in `adlb-ablfl-amb` (24 records), and including vital-sign dates in `adsl-lstalvdt-amb` (61-63 subjects). The Claude models and `gpt-oss:20b` counted days inclusively in `adsl-trtdurd-amb` and matched the oracle; both Qwen models counted elapsed days. All five matched the oracle on `adsl-saffl-amb` without asking.
3. **Agreement is not correctness.** Haiku and Sonnet produced the identical wrong output in 8 of 9 samples where both were wrong, and `gpt-oss:20b`, from a different family, produced exactly the same wrong output as the Claude models on `adae-trtemfl-amb` and `adlb-ablfl-amb`. Several independent models agreeing on a silent choice says nothing about whether the choice was the intended one.

## Offline replay of the comparator step (preview, not a harness result)

Replaying only the comparator over the same task and sample index of two models: accept the output when both produce a valid output and the two outputs are identical; otherwise flag for review. No adjudicator, no human. "Escaped" means accepted and wrong. "Caught" means flagged, with at least one of the two outputs wrong; no pair ever flagged a sample where both outputs were correct (correct outputs are identical by construction). All pairs are over the same 33 task-samples (11 tasks x 3), sorted by escaped count.

| pair | accepted | escaped (accepted and wrong) | flagged | samples with at least one wrong output | caught |
|---|---|---|---|---|---|
| Haiku + Sonnet (same family) | 32 | **8** | 1 | 9 | 1 |
| gpt-oss:20b + Haiku (different families, both strong) | 29 | **6** | 4 | 10 | 4 |
| gpt-oss:20b + Sonnet (different families, both strong) | 29 | **6** | 4 | 10 | 4 |
| gpt-oss:20b + qwen3-coder:30b | 21 | 5 | 12 | 17 | 12 |
| qwen3-coder:30b + qwen2.5-coder:7b (same family) | 15 | 5 | 18 | 23 | 18 |
| qwen3-coder:30b + Haiku | 19 | 3 | 14 | 17 | 14 |
| qwen3-coder:30b + Sonnet | 19 | 3 | 14 | 17 | 14 |
| gpt-oss:20b + qwen2.5-coder:7b | 13 | 2 | 20 | 22 | 20 |
| qwen2.5-coder:7b + Haiku | 13 | 2 | 20 | 22 | 20 |
| qwen2.5-coder:7b + Sonnet | 13 | 2 | 20 | 22 | 20 |

How to read it:

- **Mixing families did not help much when both models were strong.** The two strong models from different families (`gpt-oss:20b` with a Claude model) let 6 of 33 wrong outputs through, close to the 8 of the same-family Claude pair. The pairs with 2 to 3 escapes all include a weaker Qwen model.
- **The "caught" column is confounded by accuracy:** a pair that includes a weak model flags more simply because that model is wrong more often, so more flags does not mean independent checking.
- **The escapes are the ambiguity-consensus errors.** The 6-8 escapes of the strong pairs are essentially `adae-trtemfl-amb` and `adlb-ablfl-amb` (3 samples each) where all strong models chose identically, plus `adsl-lstalvdt-amb` for the Claude pair. A comparator cannot see an error that every programmer makes the same way.
- 11 tasks (5 ambiguous), 3 samples each; samples of one task are not independent. Treat the contrast as an indication, not a measurement; no confidence intervals are given because the samples are too correlated for them to mean much.
- The real harness (adjudicator, escalation, isolation per programmer) is not built yet; this replay uses the comparator logic only.

## Does offering the escalation option matter? (gpt-oss:20b, prompt k2-v1 versus k2-v2)

`gpt-oss:20b` also ran these 11 tasks under the old prompt that has no escalation option (`gptoss20b_v1_no_escalate_option/`; this arose from a config mistake, see `results/k2_local/summary.md`). Under both prompts, per task: identical results for 10 of 11 tasks; `adae-lastdose-std` was 3 correct without the option and 2 correct, 1 loud with it (an unrelated date-type bug). Overall v1 gave 24 correct, 9 silent; v2 gave 23 correct, 9 silent, 1 loud. In the 32 samples with a valid output under both prompts, the output was **identical in all 32**. Offering the option changed nothing for this model, and it never used it (0 escalations). One model, one option wording; this does not show that no wording could elicit escalation.

## Caveats
- The "errors" on the ambiguous tasks are silent resolutions of a genuinely open question; the oracle's reading is the standard admiral behavior, not the only defensible one. That is the finding: the models chose without saying so.
- 11 tasks designed to be harder; not a random sample of real work. One benchmark version, one study's public data.
