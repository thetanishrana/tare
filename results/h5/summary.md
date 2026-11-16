# H5: held-out ophthalmology slice, Claude pair, and the E8c competing-readings reviewer

Run 2026-11-04. Design fixed before any run (`docs/09_DECISIONS.md`, "E8c design", 2026-11-04). The six held-out ophthalmology tasks (round `ho1`: 2 ambiguous, 4 clear), 10 samples each, 60 pair runs. Programmers: Claude Haiku 5.5 (A) and Sonnet 5.5 (B), Python, prompt `k2-v4`; Sonnet 5.5 as adjudicator and, live, as reviewer v1. The same logged programmers were then replayed with the reviewer off (to define the would-be silent errors) and with reviewer v2 (`replay_reviewer_off/`, `replay_reviewer_v2/`; per-pair records in `scores.jsonl`). No prompt, reading, spec or task was changed after the first look.

**Cost: $2.0212** (live run $1.0474, reviewer-off replay $0.0581, reviewer-v2 replay $0.9157). The estimate given before the run was about $1.5; the v2 reviews were the overrun (long JSON replies, about $0.024 each), and the total passed the $2 line by about 1%. Logged in the spend table.

## Results

| | ambiguous pairs (20) | clear pairs (40) |
|---|---|---|
| reviewer off (replay) | 18 escalated, 2 right by luck (matches the oracle's reading, no question), 0 silent errors | 38 correct, 2 escalated |
| reviewer v1 (live) | 20 escalated | 35 correct, 5 escalated |
| reviewer v2 (replay) | 20 escalated | 22 correct, 18 escalated |

**The reviewer question is not answerable on this slice.** The programmers (prompt v4) asked on 18 of the 20 ambiguous pairs themselves, and the two remaining pairs matched the oracle's reading. The reviewer was therefore consulted on 38 pairs, only 2 of them ambiguous, and there were **0 would-be silent errors** (the pre-registered minimum for a claim is 10). Reported as underpowered, with the raw counts above.

Of the pairs the reviewer did see: both reviewers escalated both right-by-luck pairs. On the 36 consulted clear pairs, v1 asked on 3 (8%) and v2 on 16 (44%).

## Against the pre-registered hypotheses

- **H1 (v2 catches at least 70% of would-be silent errors with at most 10% false alarms):** the catch part is untestable (0 would-be silent errors); the false-alarm part fails (v2 44%).
- **H2 (v2 beats v1 on catches without more than 5 points more false alarms):** not supported; v2 asked on 36 points more clear pairs than v1, and there were no silent errors to compare on.
- **H3 (v2 catches the shared-stated-assumption cases v1 passed):** untestable here; no such pair arose.

v2 asked most on `adsl-studyeye-std` (6 of 10) and `adae-aestudyeye-std` (5 of 6). Whether those questions name real residual gaps in the clear specs was not checked pair by pair.

## What else the run shows

- With the check off, the Claude pair with prompt `k2-v4` raised a question on 18 of 20 ambiguous held-out pairs and on 2 of 40 clear ones, and produced no silent error. On the dev tasks the same setup escalated 9 of 21 (H4 replay, one sample). The ophthalmology ambiguities are more salient to the programmers, or these two tasks are easier to notice; two tasks and ten correlated samples each cannot separate the two.
- The frozen rule held: nothing about the reviewer prompt, the readings or the specs was adjusted after seeing these results. Further changes to v2 would need a new design entry and fresh tasks.

## Limits

Only two ambiguous tasks and samples per task are correlated; same-family pair; the slice's oracle is our own admiral-function script; labels and readings by one author; one reviewer model.
