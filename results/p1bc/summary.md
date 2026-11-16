# P1b and P1c: four more ambiguous/clear pairs and four edge-exposure pairs, local models

Run 2026-10-28. 16 tasks, 3 samples each, prompt `k2-v2` (the model may reply `ESCALATE: <question>`), up to 2 repairs, temperature 0.2, local models only (cost $0): qwen3-coder:30b and gpt-oss:20b (8192 max tokens).

- P1b (round `p1b`, standard data): `adae-astdy`, `adae-adurn`, `adlb-pchg`, `adlb-anrind`, each as `-amb` and `-std`.
- P1c (round `p1c`, perturbed inputs `pert-edge`): edge twins `adsl-saffl-edge`, `adsl-trtsdt-edge`, `adae-trtemfl-edge`, `adlb-ontrtfl-edge`, each `-amb` and `-std`. The specs are the same text as the originals; only the inputs differ (blank last dose dates, missing doses, partial start dates; see `r/perturb.R`).

Purpose: check the new tasks behave and see whether the open points that did not change the output on the standard data now do. Not a model ranking. Configs, manifests and score records are in `qwen3coder30b/` and `gptoss20b/` here.

## Results (24 samples per cell)

| Model | clear twins | ambiguous tasks | escalations |
|---|---|---|---|
| qwen3-coder:30b | 23 correct, 1 silent error | 1 correct, 23 silent errors | 0 of 48 |
| gpt-oss:20b | 24 correct | 5 correct, 19 silent errors | 0 of 48 |

Silent errors on ambiguous tasks that equal a stored defensible reading (`matches_reading`): qwen 22 of 23, gpt-oss 19 of 19. Class stays `silent_error`: the choice was still unflagged. The only unmatched sample is qwen `adlb-anrind-amb` sample 0.

## Frontier models on the same 16 tasks (added 2026-10-28)

Claude Haiku 5.5 and Sonnet 5.5, same tasks, prompt and 3 samples (no sampling parameters sent; max 16000 tokens). Cost: Haiku $0.0409, Sonnet $0.4622.

| Model | clear twins | ambiguous tasks | escalations |
|---|---|---|---|
| Claude Haiku 5.5 | 24 correct | 8 correct, 16 silent errors | 0 of 48 |
| Claude Sonnet 5.5 | 24 correct | 14 correct, 8 silent errors, 2 escalated | 2 of 48 |

"Correct" on an ambiguous task means the output equals the oracle's reading with no flag raised. All 16 Haiku and all 8 Sonnet silent errors equal a stored defensible reading.

- Sonnet's two escalations are the first Claude escalations on this benchmark that were not prompted by the E8 prompts. Both were on `adae-trtemfl-edge-amb` and both named the exact open point: whether an AE is treatment-emergent when the last dose date is missing but the first dose date is present, with the two options spelled out. The third sample proceeded silently with the compound reading (`strict-after-and-missing-end-excluded`).
- Open points that stay unflagged for both Claude models on every sample: `adlb-ontrtfl-edge-amb` (missing last dose date, `missing-end-excluded`) and `adsl-trtsdt-edge-amb` (`any-record`). Haiku also took the non-oracle reading on `adlb-pchg-amb` (3 of 3) and `adsl-saffl-edge-amb` (3 of 3, `missing-dose-counts`); Sonnet matched the oracle on `adlb-pchg-amb` and in 2 of 3 on `adsl-saffl-edge-amb`.
- Haiku `adae-trtemfl-edge-amb`: 3 of 3 compound reading, never flagged.
- `adae-astdy-amb` and `adlb-anrind-amb`: both Claude models matched the oracle's reading in every sample (no divergence, no flag), unlike the local models.
- Claude clear twins: 48 of 48 correct, so any divergence on the ambiguous twin is about the open point.

## By task (local models)

- Same non-oracle choice from both models on every sample: `adlb-pchg-amb` (PCHG on all records, `all-records`), `adlb-ontrtfl-edge-amb` (missing last dose date means not on treatment), `adsl-trtsdt-edge-amb` (any exposure record counts, including missing dose), `adae-trtemfl-edge-amb` (first dose day excluded and missing last dose date means not flagged, together).
- `adsl-saffl-edge-amb`: gpt-oss counted records with a missing dose (`missing-dose-counts`); qwen counted any active-drug record (`active-drug-any-dose`). Different unflagged choices on the same open point.
- `adae-astdy-amb`: both models took day 0 for the first dose day (`day-zero`), except one gpt-oss sample (`always-plus-one`). `adae-adurn-amb`: qwen 3 of 3 took elapsed days (`elapsed`); gpt-oss matched the oracle's inclusive count in 2 of 3 (right by luck, unflagged).
- `adlb-anrind-amb`: gpt-oss 3 of 3 matched the oracle (a result equal to a limit is normal); qwen 1 of 3 correct, 1 `no-range-normal`, 1 silent with no stored reading.
- Clear twins: all 24 gpt-oss samples correct; qwen missed one (`adae-trtemfl-edge-std`). The clear specs hold on edge data for both models, so divergence on the ambiguous twin is about the open point, not about the edge data.
- No model escalated in any of 96 samples.

## Notes and caveats

- Two stored readings were added after seeing qwen's outputs (`adae-trtemfl-edge-amb` compound reading, `adsl-saffl-edge-amb` active-drug-any-dose). The reading set was therefore extended using the very samples it is now matched against; the numbers above are with the extended set. Without them, qwen's 6 samples on those two tasks would be unmatched. Defensible readings were otherwise written before the runs.
- Local models only, 3 correlated samples per task, 8 task pairs; ambiguity labels and readings were written by one author (no external rating). Frontier models were not run on these tasks.
- gpt-oss latency is not meaningful (the machine slept during the run).
