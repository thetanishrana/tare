# E8b: can a reviewer reading the programmer's assumptions decide what to escalate?

Run 2026-10-28, local reviewers only (cost $0). Design fixed and committed before any run (`docs/09_DECISIONS.md`, "E8b design"). The reviewer sees only the task spec and the programmer's `ASSUMPTIONS:` list (no code, no oracle, no ambiguity note) and replies `ESCALATE: <question>` or `PROCEED` (prompt `REVIEWER_PROMPT` in `tare/prompts.py`, written once, not tuned). Inputs are the 85 logged `k2-v4` assumption lists from E8 (Haiku 5.5, Sonnet 5.5, qwen3-coder:30b; 11 tasks, 5 ambiguous, 3 samples; programmer escalations are not reviewed). Reviewers: qwen3-coder:30b and gpt-oss:20b, temperature 0.2. Per-review records: `qwen3-coder_30b/reviews.jsonl`, `gpt-oss_20b/reviews.jsonl`; tables from `scripts/e8_review_report.py`.

## Results

Ask counts, ambiguous / clear. "Own" is the programmer's own `k2-v4` ask (15 ambiguous, 18 clear samples per model). "Pipeline" is programmer asks or reviewer asks, out of 15 and 18.

| reviewer | programmer lists | own | reviewer (reviewed) | pipeline |
|---|---|---|---|---|
| qwen3-coder:30b | Haiku 5.5 | 4/15, 2/18 | 5/11, 7/16 | 9/15, 9/18 |
| qwen3-coder:30b | Sonnet 5.5 | 0/15, 1/18 | 2/15, 3/17 | 2/15, 4/18 |
| qwen3-coder:30b | qwen3-coder:30b | 0/15, 7/18 | 0/15, 0/11 | 0/15, 7/18 |
| gpt-oss:20b | Haiku 5.5 | 4/15, 2/18 | 11/11, 14/16 | 15/15, 16/18 |
| gpt-oss:20b | Sonnet 5.5 | 0/15, 1/18 | 15/15, 15/17 | 15/15, 16/18 |
| gpt-oss:20b | qwen3-coder:30b | 0/15, 7/18 | 14/15, 3/11 | 14/15, 10/18 |

Reviewer alone, all lists pooled: qwen3-coder:30b asked on 7 of 41 reviewed ambiguous samples (17%) and 10 of 44 clear ones (23%); gpt-oss:20b asked on 40 of 41 ambiguous (98%) and 32 of 44 clear (73%).

## Against the pre-registered hypotheses

- **H1 (pipeline ask rate on ambiguous samples exceeds the programmer's own for every programmer model): supported with the gpt-oss reviewer only**, which asks on nearly everything; with the qwen reviewer it holds for Haiku (9 vs 4) and Sonnet (2 vs 0) but not for qwen's own lists (0 vs 0).
- **H2 (false escalations on clear samples at or below 25%): not supported by any reviewer-programmer pair except Sonnet's lists with the qwen reviewer** (4/18, 22%), where the pipeline barely asks on ambiguous samples (2/15). The others range from 39% to 89%.
- **H3 (the reviewer's questions name the first-dose-day boundary on `adae-trtemfl-amb` and `adlb-ablfl-amb` in at least half of the reviews): split.** gpt-oss named it on `adae-trtemfl-amb` in 8 of 9 reviews and on `adlb-ablfl-amb` in 3 of 7 (the rest asked about tie-breaking only); qwen named it in 1 of 9 and 0 of 7. Counts were read from the questions by hand; the lists were not checked for whether each one contained the point.

## What it shows

1. **Neither reviewer separated ambiguous from clear specs.** qwen3-coder:30b as reviewer was a little more likely to ask on clear samples than on ambiguous ones; gpt-oss:20b asked on almost all of both. This is the failure mode the design warned about (a reviewer that escalates on everything passes H1 and fails H2). A usable reviewer must discriminate, and neither does with this one prompt.
2. **The assumptions lists carry the information, but this reviewer does not extract it.** gpt-oss named the first-dose-day boundary in 8 of 9 `adae-trtemfl-amb` reviews while also asking about tie-breaks and unrelated defaults on clear tasks.
3. Open next questions, none run: a stronger reviewer (Claude Haiku 5.5 would cost about $0.03 for these 85 lists; the design said to run it only if a local reviewer showed signal, and none did), a reviewer that must list the competing readings and whether each changes any output on the data, or a reviewer that sees the sample data.

## Limits

85 reviews, correlated samples, 5 ambiguous tasks, labels by one author, one reviewer prompt, two local reviewers only, no external rating. The reviewed samples are the ones where the programmer did not already ask, so the pipeline rows mix 2 sources of asking.
