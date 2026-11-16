# P1g and P1h spot check: the 11 tasks added after the last model run

Run 2026-11-05. Claude Haiku 5.5 and Sonnet 5.5, single programmer, prompt `k2-v2` (optional `ESCALATE:` reply), 1 sample per task, no sampling parameters. Tasks: `advs-ablfl`, `adae-aendt-pdates`, `adsl-dispdates`, `advs-chg`, `adlb-shift1` (each clear and ambiguous) and `adae-lastdose-amb`. Cost: Haiku $0.0138, Sonnet $0.1696. A sanity check for ill-posed specs and for stored readings the models do not land on, **not a measurement** (one sample per task).

| Model | clear twins (5) | ambiguous tasks (6) |
|---|---|---|
| Claude Haiku 5.5 | 5 correct | 1 correct (matches the oracle's reading, no question), 3 silent errors, 2 escalated |
| Claude Sonnet 5.5 | 5 correct | 1 correct (same), 5 silent errors, 0 escalated |

- **No ill-posed clear spec:** all 10 clear-twin samples were correct, including the two hard ones (`adae-aendt-pdates-std` needed one repair for Haiku; `advs-chg-std`).
- **Four of the eight silent errors matched no stored reading at first** and were each a defensible reading or a compound of two: `advs-ablfl-amb` (Haiku: pooled over time points and strictly before the first dose), `advs-chg-amb` (Haiku: pooled baseline and a value on every record), `adae-aendt-pdates-amb` (Sonnet: the death or completion date caps the imputed date even when it lies before the partial period) and `adae-lastdose-amb` (Sonnet: a record without an end date is a single dose day, for both targets). I added them as stored readings (`pooled-strict-before`, `pooled-all-records`, `cap-anywhere`, `open-records-single-day`); with them all 8 silent errors equal a stored reading. **These readings were added after seeing these outputs**, like the earlier ones noted in `results/p1bc/summary.md`, so the match rate here is not independent of the samples.
- Two Haiku escalations (`adae-aendt-pdates-amb`, `adae-lastdose-amb`); neither model escalated on `advs-ablfl-amb`, `advs-chg-amb` or `adlb-shift1-amb`.
- `adlb-shift1-amb`: both models wrote a missing value instead of the word `NULL` when a category was missing (`missing-as-null-value`).
