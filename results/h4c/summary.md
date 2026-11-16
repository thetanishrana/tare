# H4c: third sample of the Claude pair run

Run 2026-11-06. `configs/h4c_claude_pair.yaml` is the H4 and H4b configuration unchanged (Haiku 5.5 and Sonnet 5.5 programmers, prompt `k2-v4`, Sonnet 5.5 adjudicator and reviewer, 21 ambiguous tasks and 20 clear twins, 1 sample). `replay_reviewer_off/` replays the same logged programmers with the reviewer off (`configs/h4c_replay_reviewer_off.yaml`). Cost computed from the logged token counts with `tare.pricing`: $0.8787 for the pair run and $0.0247 for the replay, $0.9034 in all (a little above the $0.8 estimate, under the $2 line). Per-pair records: `claude_pair/scores.jsonl`, `replay_reviewer_off/scores.jsonl`. One sample: indicative.

## Results

| | ambiguous (21) | clear twins (20) |
|---|---|---|
| Check on | 16 escalated (4 by a programmer, 10 by the reviewer, 2 by the adjudicator), 2 correct with no question, 3 silent errors | 20 correct, 0 escalated |
| Check off (replay) | 5 escalated, 6 correct with no question, 10 silent errors | 20 correct |

- Of the 10 would-be silent errors (check off), 7 were escalated with the check on (6 by the reviewer: `adlb-ablfl-amb`, `adlb-ontrtfl-edge-amb`, `adsl-eosstt-amb`, `adsl-saffl-edge-amb`, `adsl-trtsdt-edge-amb`, `advs-average-amb`; 1 by the adjudicator on disagreeing outputs: `adlb-chg-amb`). 3 remained silent errors.
- The 3 remaining: `adae-trtemfl-amb` and `adlb-ontrtfl-amb` (both programmers agree, the first-dose-day boundary again, as in H4 and H4b) and `adsl-lstalvdt-amb` (outputs disagreed and the adjudicator accepted programmer B's).
- No false alarm on the 20 clear twins.

## Over three samples (H4, H4b, H4c)

Silent errors on the 21 ambiguous tasks, check off then on: 6 to 2, 8 to 3, 10 to 3; 24 to 8 in all. Clear-twin false alarms: 1, 0, 0 of 20 each (1 of 60). The first-dose-day boundary cases (`adae-trtemfl-amb`, `adlb-ontrtfl-amb`) passed in all three samples. Samples are not independent in the sense that matters: same 41 tasks, same models, and the tasks and readings were shaped by earlier runs of those models.
