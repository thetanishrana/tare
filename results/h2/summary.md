# H2: the H1 pair with the assumption check on and Claude Sonnet 5.5 as adjudicator and reviewer

Run 2026-10-29. `configs/h2_pair_assumption_check.yaml`: the H1 programmers (qwen3-coder:30b as A, gpt-oss:20b as B, local) now on prompt `k2-v4` (required `ASSUMPTIONS:` list, checklist, optional `ESCALATE:` reply); when their outputs agree, Claude Sonnet 5.5 reads both assumption lists with the spec (the E8b reviewer prompt) and may escalate; when they disagree, Sonnet 5.5 is the adjudicator. The same 12 p1a tasks, 1 sample. Cost: $0.0488 (7 Sonnet calls: 5 reviews, 2 adjudications); programmers local. A smoke run, not a measurement. Per-pair records in `scores.jsonl`; calls in the untracked run directory.

## Results (compare H1: `results/h1/summary.md`)

| | H1 (v2, no check, gpt-oss adjudicator) | H2 (v4, assumption check, Sonnet adjudicator) |
|---|---|---|
| ambiguous pairs escalated | 1 of 6 | **5 of 6** |
| ambiguous pairs accepted wrong (silent error) | 4 | 1 |
| ambiguous pairs accepted right by luck | 1 | 0 |
| clear twins escalated (false alarm) | 0 of 6 | **3 of 6** |
| clear twins accepted correct | 6 | 3 |

Where the escalations came from in H2:
- **Programmers' own questions (v4 prompt): 5 of the 8 escalations.** qwen asked on 4 ambiguous and 1 clear pair, gpt-oss asked on 1 ambiguous pair (as in E8, the v4 prompt makes qwen ask a lot, not always about the right point).
- **Assumption check (Sonnet reviewer): 3 of the 8.** Of 5 reviews it escalated `adlb-ontrtfl-amb` (it named the unsettled boundary of "between" the first and last dose, the point that moves the oracle's answer; a correct catch), but also `adae-astdt-std` and `adsl-trtsdt-std` (clear specs; its questions concerned how an implementation treated odd inputs, a false alarm each), and it let `adlb-chg-amb` through (both programmers chose `all-records`, the unflagged silent error that remains) and `adlb-chg-std` (correct).
- **Adjudicator (Sonnet): 2 calls, both picks correct** (`adae-aoccifl-std`, `adsl-eosstt-std`, both clear twins where one programmer erred).

## Reading

The check plus the v4 prompt gave much more asking on ambiguous pairs, but half the clear twins were also escalated, so the pipeline did not separate the two kinds of spec. The reviewer alone had 1 true catch, 2 false alarms and 1 miss in 5 reviews, an n too small to rate it; the large gain in H2 comes mostly from the programmers' own v4 questions. Sonnet as adjudicator picked correctly in both cases it was used (H1's gpt-oss adjudicator was wrong in both of its picks), which is suggestive only.

Limits: 12 pairs, 1 sample, two local programmers, a single prompt for the reviewer, labels by one author; H1 and H2 differ in three things at once (prompt version, adjudicator, check), so the table does not attribute effects to any one of them.
