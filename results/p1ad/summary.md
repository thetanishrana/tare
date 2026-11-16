# P1a pairs and the first ADVS pair on Claude Haiku 5.5 and Sonnet 5.5

Run 2026-10-28. 14 tasks: the six p1a ambiguous tasks and their clear twins (`adsl-trtsdt`, `adsl-eosstt`, `adae-astdt`, `adae-aoccifl`, `adlb-chg`, `adlb-ontrtfl`) and `advs-average-amb` / `advs-average-std`. Prompt `k2-v2` (optional `ESCALATE:` reply), 3 samples, up to 2 repairs, no sampling parameters sent, max 16000 tokens. Cost: Haiku $0.0455, Sonnet $0.5034. The local-model results on the six p1a pairs are in `results/p1a/summary.md`. Configs, manifests and score records: `haiku55/`, `sonnet55/` here.

## Results (21 samples per cell)

| Model | clear twins | ambiguous tasks | escalations |
|---|---|---|---|
| Claude Haiku 5.5 | 21 correct | 9 correct, 12 silent errors | 0 of 42 |
| Claude Sonnet 5.5 | 20 correct, 1 silent error | 12 correct, 9 silent errors | 0 of 42 |

"Correct" on an ambiguous task means the output equals the oracle's reading with no flag raised. All 21 silent errors on ambiguous tasks equal a stored defensible reading.

## By task

- `adlb-ontrtfl-amb`: both models, 3 of 3, counted a Baseline-visit result on the first dose day as on treatment (`baseline-day-counts`), against the oracle.
- `adsl-eosstt-amb`: both models, every sample, mapped screen failures to a status (`screenfail-discontinued`, once `screenfail-ongoing` for Sonnet) instead of leaving them missing.
- `advs-average-amb`: both models, 3 of 3, wrote no summary record for measurements without an analysis visit (`no-visit-excluded`), against the oracle.
- `adlb-chg-amb`: Haiku 3 of 3 wrote CHG on all records (`all-records`); Sonnet matched the oracle in 3 of 3.
- `adae-aoccifl-amb`, `adae-astdt-amb`, `adsl-trtsdt-amb`: both models matched the oracle's reading in every sample, unflagged.
- No model asked in any of 84 samples. Sonnet's one clear-twin error (`adsl-trtsdt-std`, sample 1) was not examined.
- The Claude models did better than the local models on the same six pairs in the ambiguous cells (local models: 6 of 36 correct across both; Claude: 21 of 42 across both), but the open points that moved the oracle's answer were still resolved without a question in 21 of 21 cases where they diverged.

## Caveats

3 correlated samples, 7 task pairs, labels and readings by one author, no external rating. The six p1a pairs were run locally before the readings for `adae-trtemfl-edge` and `adsl-saffl-edge` were extended; the stored readings used here were fixed before this run.
