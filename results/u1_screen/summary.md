# u1 screening (E9, programmers only)

Run 2026-11-08. `configs/u1_screen_haiku.yaml` and `configs/u1_screen_sonnet.yaml`: Claude Haiku 5.5 and Sonnet 5.5 as single programmers, prompt `k2-v4`, 1 sample, on the 6 ambiguous `u1` tasks. Cost: $0.0054 (Haiku) and $0.0841 (Sonnet), $0.0895 in all (estimate was under $0.15). One sample per task: a screen, not a measurement. Per-sample records: `haiku/scores.jsonl`, `sonnet/scores.jsonl`.

| task | Haiku 5.5 | Sonnet 5.5 | kept (neither asked) |
|---|---|---|---|
| `advs-ontrtfl-amb` | silent error | silent error | yes |
| `adsl-trtedt-edge-amb` | silent error | silent error | yes |
| `advs-ady-amb` | correct | correct | yes (no silent error to catch, so likely no use) |
| `adlb-r2base-amb` | escalated (BASE = 0) | correct | no |
| `advs-avisit-amb` | escalated (which visits count) | correct | no |
| `advs-anl01fl-amb` | escalated (ties on the same date) | escalated (time points separate) | no |

- Silent errors: 4 of 12 samples. Both `adsl-trtedt-edge-amb` errors equal the stored reading `any-record` (13 of 306 subjects differ from the oracle). Sonnet's `advs-ontrtfl-amb` error equals `baseline-day-counts` (2783 records); Haiku's differs from the oracle on 2761 records and matches no stored reading (a new reading to examine, not yet added, since readings are fixed before confirmatory runs).
- Under the pre-registered rule (drop a task if either programmer asks), 3 tasks remain, below the 8 required for the confirmatory run. The rule says to extend the set before any pair run; nothing has been run in pairs.
- The screening sample is not reused in the confirmatory run.

## Second and third screening sets (2026-11-11)

Four more ambiguous tasks were built (`advs-ontrtfl-edge`, `advs-ablfl-edge`, `adae-trtemfl-pdates`, `adae-astdy-pdates`; new perturbed ADVS oracle `pert-edge-advs`) and screened the same way (`u1b_*`, $0.0612), then `advs-chg-edge` (`u1c_*`, $0.0153). Total cost of these two sets $0.0765.

| task | Haiku 5.5 | Sonnet 5.5 | kept |
|---|---|---|---|
| `advs-ontrtfl-edge-amb` | silent error (no stored reading) | silent error (no stored reading), identical output | yes |
| `advs-ablfl-edge-amb` | silent error (`pooled-strict-before`) | silent error (`strict-before`) | yes |
| `adae-trtemfl-pdates-amb` | silent error (no stored reading) | silent error (no stored reading), identical output | yes |
| `adae-astdy-pdates-amb` | correct | correct | yes (no silent error to catch) |
| `advs-chg-edge-amb` | escalated | escalated | no |

- Kept over all three sets: `advs-ontrtfl`, `adsl-trtedt-edge`, `advs-ady`, `advs-ontrtfl-edge`, `advs-ablfl-edge`, `adae-trtemfl-pdates`, `adae-astdy-pdates`: 7, one short of the 8 the design requires. Two of these (`advs-ady`, `adae-astdy-pdates`) were answered correctly by both programmers and are unlikely to yield would-be silent errors.
- Both programmers gave the same wrong output on `advs-ontrtfl-edge-amb` (3880 records differ from the oracle) and on `adae-trtemfl-pdates-amb` (186 records), and neither output equals a stored reading: the stored readings for these two tasks are incomplete. Readings are not changed before the confirmatory run (pre-registered); these cases are reported as silent errors with no matching reading.
- A candidate `adlb-ablfl-edge` was dropped before screening: only one stored reading differed from the oracle (admission rule: at least two).

## Fourth set (2026-11-11)

`adae-aoccifl-aedates` (the `adae-aoccifl` rule ported to the perturbed AE-date oracle `pert-aedates`; references correct, three stored readings differing on 70, 230 and 414 of 1191 events) screened as `u1d_*`, $0.0149: Haiku 5.5 escalated, Sonnet 5.5 correct. Dropped under the rule (either programmer asks). Kept count unchanged at 7 of 12 built.

## Fifth and sixth sets (2026-11-11)

- `adlb-ablfl-edge` (the `adlb-ablfl` rule on the perturbed exposure oracle, readings `strict-before` 32 and `by-visit-number` 132 of 59580 records; `u1e_*`, $0.0140): Haiku escalated, Sonnet silent error equal to `strict-before`. Dropped.
- `adae-lastdose-edge` (the `adae-lastdose` rule on a new oracle id `pert-edge-adae`; readings differ on 972, 871, 117 and 117 of 1191 events; `u1f_*`, $0.0222): both programmers escalated. Dropped. The existing `pert-edge` ADAE has last-dose columns built from the unperturbed EX (a flaw for last-dose tasks only; TRTEMFL and the other dose-date tasks on it use the perturbed ADSL and are unaffected), hence the new oracle id.
- Kept count unchanged: 7 of 14 built.
