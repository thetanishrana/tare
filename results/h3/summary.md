# H3: the assumption check in isolation (replay of the H2 programmers)

Run 2026-10-29. The H2 programmers (qwen3-coder:30b as A, gpt-oss:20b as B, prompt `k2-v4`, 12 p1a tasks, 1 sample) were replayed from the logged responses of `results/h2/` (code re-run in the sandbox, no programmer call repeated), and only the decision stage changed: Claude Sonnet 5.5 stays the adjudicator and the assumption reviewer varies. Configs `configs/h3_review_<variant>.yaml`; the Sonnet reviewer is the H2 run itself. Cost of the four replays: $0.0799 (Sonnet adjudication and Haiku review calls; local reviewers free). A smoke comparison on 5 reviewed pairs, not a measurement.

## What the reviewer saw

The reviewer is consulted only when both programmers produced valid output, neither asked, and the outputs agree. In this set that is 5 pairs: 2 ambiguous (`adlb-chg-amb`, `adlb-ontrtfl-amb`, both a silent error if nobody asks) and 3 clear twins (`adae-astdt-std`, `adlb-chg-std`, `adsl-trtsdt-std`). Every other pair is decided before the reviewer matters (a programmer asked, or the outputs disagreed and Sonnet adjudicated).

| reviewer | asked on the 2 ambiguous | asked on the 3 clear | silent errors left (of 12) | ambiguous pairs escalated (of 6) | clear pairs escalated (of 6) |
|---|---|---|---|---|---|
| none | 0 | 0 | 2 | 4 | 1 |
| qwen3-coder:30b | 0 | 0 | 2 | 4 | 1 |
| Claude Haiku 5.5 | 0 | 2 | 2 | 4 | 3 |
| Claude Sonnet 5.5 (H2) | 1 (`ontrtfl`) | 2 | 1 | 5 | 3 |
| gpt-oss:20b | 2 | 2 | 0 | 6 | 3 |

(The clear pair escalated with no reviewer is `adlb-ontrtfl-std`, where qwen asked.)

## Reading

- **No reviewer separated the two kinds of spec on this sample.** The only one that caught both silent errors (gpt-oss:20b) also flagged two of the three clear pairs; qwen3-coder:30b never asked; Haiku asked only on clear pairs. Sonnet caught one of two.
- **The same two clear pairs were flagged by gpt-oss, Haiku and Sonnet** (`adae-astdt-std`, `adsl-trtsdt-std`). They may reflect real residual points in those specs that the programmers wrote into their lists, not random noise (as in E8, where some "false" escalations named real gaps). That was not checked pair by pair here.
- **The assumption check changed little overall.** With no reviewer the pipeline already escalated 4 of 6 ambiguous pairs, because the v4 programmers asked themselves; the check adds at most the 2 pairs where both programmers agreed on the same unflagged choice. That is the case it exists for, and in 5 pairs it was decided by a coin-flip-sized sample.

## Limits

5 reviewed pairs, one sample, the same two local programmers, one reviewer prompt, labels by one author. The result is that the question is not settled: a proper test needs many more agreeing-and-wrong pairs, which means more tasks with agreement on an unflagged choice (the `edge` and ADLB tasks produce them) and several samples, ideally with Claude programmers.
