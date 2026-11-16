# H1: first double-programming run, local models

Run 2026-10-29 (local, $0). `configs/h1_local_pair.yaml`: programmer A qwen3-coder:30b and programmer B gpt-oss:20b (both Python, prompt `k2-v2` with the optional `ESCALATE:` reply), gpt-oss:20b as the model adjudicator, no assumption check. The 12 p1a tasks (6 ambiguous, 6 clear twins), 1 sample each, so 12 pair runs. Harness code: `tare/harness.py`; every call is in `calls.jsonl` of the run directory (not tracked), per-pair records in `scores.jsonl` here. A smoke run of the harness on real models, not a measurement.

## Results

| | pairs | accepted by agreement | accepted by adjudicator verdict | escalated | outcome against the oracle |
|---|---|---|---|---|---|
| clear twins | 6 | 6 | 0 | 0 | 6 correct |
| ambiguous tasks | 6 | 3 | 2 | 1 | 1 correct (matches the oracle's reading, no question asked), 4 silent errors, 1 escalated |

- **Agreement did not mean right.** On `adlb-chg-amb` and `adlb-ontrtfl-amb` both programmers made the same non-oracle choice (`all-records`, `baseline-day-counts`), the comparator saw no difference, and the harness accepted a wrong output with nothing flagged. This is the failure the assumption check was designed to address; it was off in this run, so it is unmeasured here.
- **The adjudicator picked a side instead of escalating** on `adae-aoccifl-amb` (the output matches stored reading `lowest-aeseq`) and `adae-astdt-amb` (a reading with no stored match), choosing B (its own model family, gpt-oss) both times, and both choices were wrong against the oracle. One escalation (`adsl-eosstt-amb`, asking which `DSDECOD` values count as completed or discontinued).
- Net: the pipeline escalated on 1 of 6 ambiguous pairs and turned 4 into silent errors; no better than a single programmer on the same tasks (local single-model results: `results/p1a/summary.md`).

## Caveats

12 pairs, 1 sample; one pair of local models and the adjudicator is the same model as programmer B, so a self-preference (2 of 2 verdicts for B) cannot be separated from chance; the unmatched `adae-astdt-amb` output was not inspected; labels by one author. Programmers A and B are different families but both are far from frontier.
