# P1a: six new ambiguous tasks and their clear twins, local models

Run 2026-10-27. 12 tasks (round `p1a`: `adsl-trtsdt`, `adsl-eosstt`, `adae-astdt`, `adae-aoccifl`, `adlb-chg`, `adlb-ontrtfl`, each as an `-amb` task and its existing `-std` clear twin, same oracle), 3 samples each, prompt `k2-v2` (the model may reply `ESCALATE: <question>`), up to 2 repairs, temperature 0.2. Local models only (cost $0): qwen3-coder:30b and gpt-oss:20b (8192 max tokens). Configs, manifests and score records are in `qwen3coder30b/` and `gptoss20b/` here. Purpose: check that the new tasks behave (twins solved, ambiguous ones diverge), not to rank models.

## Results (18 samples per cell)

| Model | clear twins | ambiguous tasks | escalations |
|---|---|---|---|
| qwen3-coder:30b | 15 correct, 3 silent errors | 3 correct, 11 silent errors, 4 loud errors | 0 of 36 |
| gpt-oss:20b | 18 correct | 3 correct, 13 silent errors, 1 loud error, 1 escalated | 1 of 36 |

Silent errors on ambiguous tasks that equal a stored defensible reading (`matches_reading`): qwen 7 of 11 (`adlb-chg-amb` 3 `all-records`, `adlb-ontrtfl-amb` 3 `baseline-day-counts`, `adae-astdt-amb` 1 `adjust-any-earlier`); gpt-oss 8 of 13 (`adlb-chg-amb` 3, `adlb-ontrtfl-amb` 3, `adae-aoccifl-amb` 2 `lowest-aeseq`). The class stays `silent_error`: the choice was still unflagged.

## By task

- `adsl-trtsdt-amb`: all 6 samples match the oracle's reading (placebo rows count). Right by luck; the model never flagged the choice.
- `adlb-chg-amb`, `adlb-ontrtfl-amb`: every sample from both models chose the same non-oracle reading (CHG on all records; baseline-visit result on the first dose day counts as on treatment). Same unflagged choice across two model families.
- `adsl-eosstt-amb`: qwen's three silent errors matched no stored reading; they invented disposition terms not present in the data and defaulted unseen terms to ONGOING, so they are data-handling errors, not an alternative reading. gpt-oss escalated once (asked which `DSDECOD` values mean completion or discontinuation, and about final visit terms) and made 2 silent errors.
- `adae-aoccifl-amb`, `adae-astdt-amb`: mixed; qwen had 4 loud errors here. gpt-oss `astdt-amb` silent errors (3) matched no stored reading and were not inspected.
- Twin failures: qwen `adae-aoccifl-std` 2 silent, `adsl-eosstt-std` 1 silent. These are explicit specs, so they are plain errors.

## Caveats

Local models only, 3 correlated samples per task, 6 task pairs; one author wrote the ambiguity labels and the stored readings (no external rating). Frontier models were not run on these tasks. The gpt-oss run paused for over an hour of wall-clock time when the machine slept; latency figures are not meaningful.
