# E9: reviewer on unseen ambiguous tasks (3 samples)

Run 2026-11-11, design pre-registered 2026-11-06 in `docs/09_DECISIONS.md`. Claude Haiku 5.5 (A) and Sonnet 5.5 (B), prompt `k2-v4`, Sonnet adjudicator; the 7 `u1` ambiguous tasks that passed screening and their 7 clear twins, 3 fresh samples: 42 pair runs (21 ambiguous, 21 clear). R1 is the assumptions reviewer (reviewer v1, live in `claude_pair/`); `replay_reviewer_off/` and `replay_reviewer_v2/` replay the same logged programmers with no reviewer and with R2, the competing-readings reviewer (`REVIEWER_PROMPT_V2`, unchanged from E8c). Cost computed from logged token counts: $0.8306 (pair run), $0.0255 (reviewer off), $0.9456 (R2 replay), $1.8017 in all (estimate $1.55; the R2 replay ran about $0.35 over its $0.6 estimate). **Deviation from the design: 7 tasks, not the 8 the design required** (the screening step kept 7 of 14 built; see `results/u1_screen/summary.md`). The tasks were written after seeing where the programmers stay quiet, and the 7 are not independent of the dev findings.

## Outcomes

| | ambiguous (21 pairs) | clear twins (21 pairs) |
|---|---|---|
| Reviewer off | 3 escalated, 6 correct, **12 silent errors** | 21 correct |
| R1 on (live) | 9 escalated (1 by a programmer, 3 by the adjudicator, 5 by the reviewer), 5 correct, 7 silent errors | 21 correct, 0 escalated |
| R2 (replay) | 21 escalated | 12 escalated, 9 correct |

- **Would-be silent errors: 12**, from 4 tasks with 3 samples each (`adae-trtemfl-pdates-amb`, `adsl-trtedt-edge-amb`, `advs-ontrtfl-amb`, `advs-ontrtfl-edge-amb`); in all 12 the two programmers agreed on the same output and neither asked. The pre-registered minimum of 10 is met, but the 12 are 4 tasks, so the effective sample is small and clustered. The other 3 ambiguous tasks gave no would-be silent errors: `advs-ady-amb` and `adae-astdy-pdates-amb` were answered correctly (both programmers), `advs-ablfl-edge-amb` drew a question every time.
- Stored readings: the 3 `adsl-trtedt-edge-amb` errors equal `any-record`; the 9 errors on the other three tasks equal no stored reading (the programmers resolved missing end dates, first-dose-day boundaries or imputed dates in combinations the stored readings do not cover). Readings were not changed (pre-registered).

## Pre-registered hypotheses

| | rule | result |
|---|---|---|
| H1 | R1 escalates on at least 50% of the would-be silent errors with at most 5% false alarms | **Not met**: 5 of 12 (42%); 0 of 21 false alarms. By task: `adsl-trtedt-edge` 3 of 3, `advs-ontrtfl` 1 of 3, `advs-ontrtfl-edge` 1 of 3, `adae-trtemfl-pdates` 0 of 3 |
| H2 | R2 escalates on strictly more would-be silent errors than R1, with at most 5 points more false alarms | **Not met**: R2 escalated 12 of 12 (more than R1's 5), but on 12 of 21 clear pairs (57%) against R1's 0 of 21 |
| H3 | R2 escalates on at least half of the shared-stated-assumption pairs | **Met, with a caveat**: R2 escalated on all 12 would-be silent errors, including the 7 that R1 passed. The assumption lists of sample 0 of each of the 4 tasks were read and in each both lists state the same choices; the other 8 pairs' lists were not read, so "all 12 are shared-stated-assumption pairs" is assumed, not checked |
| H4 | report R2's false-alarm rate | 12 of 21 clear pairs (57%); R2 escalated on 33 of 42 pairs overall, so it separates ambiguous from clear poorly (H5: 16 of 36 clear pairs) |

## Reading

R2 catches everything and R1 catches under half, but R2's catch rate comes from asking almost always (33 of 42 pairs), which is not a usable reviewer; R1 stays quiet on clear specs (0 of 21, 1 of 60 over H4 to H4c as well as these) and catches about 40 to 60% of the would-be silent errors across studies (H4 to H4c: 15 of 23; here 5 of 12). Silent errors on the ambiguous tasks went from 12 to 7 with R1 on (reviewer-off replay to live run). The shared-stated-assumption blind spot again showed up for R1, on a set of tasks it had not been tuned on (`adae-trtemfl-pdates`: 0 of 3, both programmers wrote `ASTDT > TRTSDT` with a reason). Limits: 7 tasks, 4 of which produced all the would-be silent errors, 3 samples each (correlated), same-family pair, single-author tasks and labels.
