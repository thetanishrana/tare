# K2, frontier arm: Claude Haiku 5.5 and Sonnet 5.5 on the 20 K2 tasks

Run 2026-10-26 via the Anthropic API. 20 tasks x 1 sample each, Python, up to 2 repairs for loud errors, benchmark 0.1.0, prompt `k2-v1`. Run directories (local, git-ignored): `results/20261026-185407_k2_haiku55/` and `results/20261026-185805_k2_sonnet55/`; score records, manifests and configs are copied into `haiku55/` and `sonnet55/` here.

Settings: no temperature or other sampling parameters were sent (Claude 5.5 models reject non-default values); adaptive thinking with each model's default effort (`medium` for Haiku 5.5, `high` for Sonnet 5.5); `max_tokens` 16000; no refusal fallbacks.

**K2 pass line: NOT MET.** The line was "at least 3 of 20 tasks are silent errors for at least one frontier model". Both models had 0 of 20.

| Model | correct | silent error | loud error | repairs needed | tokens in / out | cost (USD) |
|---|---|---|---|---|---|---|
| Claude Haiku 5.5 (`claude-haiku-5-5`) | 20 | 0 | 0 | 0 | 49,609 / 29,264 | 0.0196 |
| Claude Sonnet 5.5 (`claude-sonnet-5-5`) | 20 | 0 | 0 | 1 (`adae-astdt-dayonly`: loud on the first attempt, correct on the second) | 54,125 / 11,523 | 0.2235 |

Both runs scored the 10 standard and the 10 sponsor-variant tasks equally (20 of 20), so memorization of the public admiral templates does not explain the result: the variants require following the spec, and both models did. Total API spend for this arm: $0.2431 (costs computed from token counts at the list prices in `configs/pricing.yaml`; the Console balance was not checked).

## How this compares
For context, same tasks, same prompt, same sandbox: `qwen3-coder:30b` 51 of 60 samples correct with 4 silent errors (`results/k2_local/summary.md`); `qwen2.5-coder:7b` 25 of 60 (`results/k4/summary.md`). The frontier models were far better than the local ones on these tasks.

## What this does and does not show
- The tasks are well specified: each spec was written to be explicit and was checked against an independent reference solution. Real study specs are often vaguer, and Merck traced most of its remaining mismatches to ambiguous specs, so these 20 tasks probably measure the easy end. The kit has no deliberately ambiguous tasks yet.
- One sample per task per model, 20 tasks: this can rule out a high silent-error rate on this task type, but not a rare one.
- The K3 comparison for the frontier models is undefined: neither was ever wrong, so P(B wrong given A wrong) has no support.

## What the roadmap says to do
`docs/08_ROADMAP.md`: if K2 fails, add harder derivations (visit windowing, LOCF derived records, baselines with unscheduled visits, partial-date imputation variants). If those also give near-zero silent errors, drop silent-error rate as the headline and reposition around local and firewall correctness plus cost. Changing the project's scope needs an explicit decision.
