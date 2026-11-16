# H4: Claude double-programming pair on every ambiguous task and its clear twin

Run 2026-10-29. `configs/h4_claude_pair.yaml`: programmer A Claude Haiku 5.5, programmer B Claude Sonnet 5.5 (same family), both Python, prompt `k2-v4` (required `ASSUMPTIONS:` list, optional `ESCALATE:` reply); Sonnet 5.5 as adjudicator and as assumption reviewer (it reads both lists with the spec when the outputs agree and neither asked). All 21 ambiguous tasks and their 20 clear twins (`adae-astdt-pdates-amb` has no twin), 1 sample each: 41 pair runs. Cost: $0.8264 (Haiku $0.0479, Sonnet programmer $0.5749, reviewer $0.1906, adjudicator $0.0129). A replay of the same logged programmers with the reviewer off (`replay_reviewer_off/`, adjudicator Sonnet, $0.0131) shows what the check changed. Per-pair records: `claude_pair/scores.jsonl`, `replay_reviewer_off/scores.jsonl`. One sample per task: indicative, not a measurement.

## Results

| | ambiguous (21) | clear twins (20) |
|---|---|---|
| **Check on** | 16 escalated (7 by a programmer, 7 by the reviewer, 2 by the adjudicator), 3 accepted matching the oracle's reading with no question, 2 silent errors | 19 correct, 1 escalated (false alarm) |
| **Check off (replay)** | 9 escalated, 6 accepted matching the oracle's reading, 6 silent errors | 20 correct |

- The reviewer was consulted on 32 pairs (programmers' outputs agreed, nobody asked): 12 ambiguous and 20 clear. It escalated 7 of the 12 ambiguous and 1 of the 20 clear. Without it, 4 of those 7 would have been silent errors (`adlb-ontrtfl-edge-amb`, `adsl-eosstt-amb`, `adsl-saffl-edge-amb`, `adsl-trtsdt-edge-amb`) and 3 would have been accepted matching the oracle's reading with the choice unflagged (`adae-aoccifl-amb`, `adsl-saffl-amb`, `adsl-trtdurd-amb`). Its questions named the open point in each case (for example inclusive versus elapsed counting for TRTDURD, whether a dose of 0 or a missing dose counts for SAFFL, which dispositions count as discontinued).
- The check missed 2 silent errors where both programmers wrote the choice down and the reviewer still let it pass: `adae-trtemfl-amb` (strict `ASTDT > TRTSDT`, written as "read literally as strictly after") and `adlb-ontrtfl-amb` (a result on the first dose day counts), the first-dose-day boundary again.
- One false alarm on a clear twin: `adae-astdt-std`, where the reviewer asked how malformed dates should be treated, a gap the clear spec does not cover.
- Adjudicator: 2 calls on disagreeing outputs, both escalated.
- Comparator agreement alone, with the check off, accepted 6 wrong ambiguous outputs and passed 6 more only by luck.

## Reading

With Claude programmers and a Claude reviewer the assumption check discriminated much better than in H2 and H3 (local programmers, 5 reviewed pairs): 7 of 12 ambiguous pairs against 1 of 20 clear, and it cut the silent errors from 6 to 2 at the cost of one false alarm. The two it missed are the cases E8 already singled out. Reasons for caution: 1 sample, the 41 tasks were authored by one person, the reviewer prompt was written before any run but the ambiguous tasks and the reading set were shaped by earlier runs of the same models, and Haiku and Sonnet are one family (they agree often, which is what the check needs and also what a cross-family pair would reduce).

## Next

More samples (a second run costs about $0.8), a cross-family pair if an OpenAI key becomes available, Haiku and local reviewers on the same logged programmers via `replay_from` (cents), and a look at whether the two missed boundary cases can be caught by a reviewer that must name competing readings.

## Reviewer swaps on the logged programmers (added 2026-10-29)

The same logged H4 programmers replayed with other reviewers (`replay_reviewer_<name>/`; adjudicator Sonnet 5.5 throughout; the cost column counts the Claude calls only). Of the 32 pairs that reach the reviewer, 12 are ambiguous: 6 would be silent errors with no reviewer and 6 are right by luck (the oracle's reading, unflagged); 20 are clear.

| reviewer | asked on the 12 ambiguous | of the 6 silent errors | of the 6 right by luck | asked on the 20 clear | silent errors left (of 21 ambiguous) | cost |
|---|---|---|---|---|---|---|
| qwen3-coder:30b | 3 | 0 | 3 | 1 | 6 | $0.0129 |
| gpt-oss:20b | 12 | 6 | 6 | 15 | 0 | $0.0125 |
| Claude Haiku 5.5 | 10 | 4 | 6 | 10 | 2 | $0.0317 |
| Claude Sonnet 5.5 (the run above) | 7 | 4 | 3 | 1 | 2 | $0.2035 (reviews and adjudications) |

- Only Sonnet 5.5 asked on a third or more of the silent errors while staying quiet on clear specs (1 of 20). Haiku and gpt-oss asked on every right-by-luck pair but also on half or three quarters of the clear ones; qwen3-coder:30b asked on almost nothing (0 of the 6 silent errors).
- gpt-oss:20b "caught" all 6 silent errors only because it escalated almost everything (27 of 32 reviewed pairs). A reviewer that asks on 15 of 20 clear specs is not usable.
- Whether the Sonnet result is about the model or the prompt is untested: one reviewer prompt, written once, and only these 32 reviewed pairs.

## Second sample (H4b, added 2026-10-29)

An independent second run of the same 41 tasks with the same programmers, prompt, reviewer and adjudicator (`configs/h4b_claude_pair.yaml`; records in `results/h4b/`), plus a replay with the reviewer off. Cost: $0.8233 and $0.0119. Combined with H4 this gives two samples per task (not independent of the tasks and readings, which were shaped by earlier runs of the same models).

| | H4 | H4b | both |
|---|---|---|---|
| reviewed pairs (programmers agreed, nobody asked) | 32 (12 ambiguous, 20 clear) | 32 (12 ambiguous, 20 clear) | 64 |
| ambiguous pairs that would be silent errors with no reviewer | 6 | 7 | 13 |
| reviewer asked on the ambiguous reviewed pairs | 7 of 12 | 8 of 12 | 15 of 24 |
| reviewer asked on the would-be silent errors | 4 of 6 | 5 of 7 | 9 of 13 |
| reviewer asked on the clear reviewed pairs (false alarms) | 1 of 20 | 0 of 20 | 1 of 40 |
| silent errors on the 21 ambiguous tasks, check off then on | 6 → 2 | 8 → 3 | 14 → 5 |
| clear twins correct, check on | 19 of 20 | 20 of 20 | 39 of 40 |

- **The discrimination replicated:** the reviewer asked on about two thirds of the would-be silent errors and on 1 of 40 clear pairs, in both samples. Silent errors fell from 14 to 5 over the two samples at the cost of one false alarm.
- **The same two cases were missed both times:** `adae-trtemfl-amb` (strict `ASTDT > TRTSDT`) and `adlb-ontrtfl-amb` (first dose day counts). In the logged reviews the two programmers' lists agree with each other and state the choice plainly ("read literally as strict", "inclusive at both ends"), and the reviewer answered `PROCEED`. A hypothesis, not tested: when both lists state the same reading with a reason, this reviewer treats the point as settled; the check asks when lists differ or hedge. If so, a shared assumption is exactly the case it cannot catch, and it is the case double programming is weakest on.
- Four tasks were escalated by the reviewer in both samples.

Limits stay: one reviewer prompt and model, a same-family pair, 41 tasks by one author, no external rating. Two samples support "the effect replicates" for this setup, not a rate for other models or datasets.
