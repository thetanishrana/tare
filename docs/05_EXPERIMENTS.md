# Experiments

## Model roster

Model IDs and Claude prices were verified against Anthropic's docs on 2026-10-18 (see `configs/pricing.yaml`). Local model tags were verified when pulled.

| Role | Model | Where | Notes |
|---|---|---|---|
| Frontier, mid | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | Anthropic API | Main frontier programmer |
| Frontier, cheap | Claude Haiku 5.5 (`claude-haiku-5-5`) | Anthropic API | Cheap development and baseline |
| Local coder (Qwen family) | `qwen3-coder:30b` | Ollama | About 19 GB at 4-bit; mixture-of-experts, about 3B active parameters |
| Local (OpenAI family) | `gpt-oss:20b` | Ollama | About 14 GB; a free, different family from Claude and Qwen |
| Local (Mistral family) | `devstral:24b` | Ollama | About 14 GB; 46.8% on SWE-Bench Verified per its card |
| Small, trainable | `qwen2.5-coder:7b` or a Qwen 1.7–4B model | Ollama / MLX | K4 and Phase 3 |
| Optional | An OpenAI API model | OpenAI API | Only if budget allows; gpt-oss covers the OpenAI family for free |

**Pricing (verified 2026-10-18 on platform.claude.com/docs/en/about-claude/pricing).** Haiku 5.5 is $0.10 / $0.50 per million input / output tokens for prompts up to 100,000 tokens ($0.50 / $2.50 above that); Sonnet 5.5 is $2 / $10; the Batch API is 50% off; cache reads are 0.1x the input price (0.05x on Sonnet 5.5 and Opus 5.5, so $0.10 and $0.01 here for Sonnet 5.5 and Haiku 5.5 respectively as listed). Prices live in `configs/pricing.yaml` with the source and date. Model IDs: `claude-sonnet-5-5`, `claude-haiku-5-5`. Re-check before the final frozen runs.

**API call settings.** Claude 5.5 models reject non-default `temperature`/`top_p`/`top_k`, so API runs send no sampling parameters (local runs use temperature 0.2). Thinking is adaptive; effort uses each model's default (`high` for Sonnet 5.5, `medium` for Haiku 5.5) unless a config sets `effort`. Thinking tokens are billed as output tokens. Refusal fallbacks are deliberately not enabled, so a run never silently switches model.

## Configurations

| id | Setup | Answers |
|---|---|---|
| **E0** single programmer | Each model alone, R and Python | RQ1: silent-error rate per model; the baseline |
| **E1** self-review | Model writes code, then reviews its own code against the spec and may revise it | Cost-matched baseline (about 2× tokens) |
| **E2** same-family double | Two independent samples from the same model, compared and adjudicated | Within-family correlation; cost-matched |
| **E3** cross-family double | Claude + qwen3-coder (frontier + local) | RQ2 and RQ3: the main claim |
| **E4** fully local double | qwen3-coder + gpt-oss (or devstral) | The behind-the-firewall configuration |
| **E5** language diversity | E3 with A in R and B in Python, versus both in the same language | Does language diversity reduce correlation? |
| **E6** adjudication policies | Third-model adjudicator, programmer-family adjudicator, always-escalate | RQ4: escalation rate and accuracy |
| **E7** trained small model as B | Phase 3 model as programmer B | RQ5 |
| **E8** escalation elicitation | Single programmers on ambiguous and clear-twin tasks under prompt variants: baseline (`k2-v2`, an optional `ESCALATE:` reply), a stronger instruction, a required list of assumptions made, a checklist of common ambiguities, and an adjudicator that must name competing readings | RQ1b: can the ask rate rise without false escalations? Baseline measured: 0 of 165 samples asked. First round done 2026-10-27 (prompts v3, v4; Haiku, Sonnet, qwen3-coder:30b): `results/e8/summary.md` |

Fixed settings (record them in every config): temperature (start at 0.2), maximum output tokens, `max_repairs = 2`, **3 samples per task** for variance, the prompt template version, the data-description version.

## Metrics

| Metric | Definition |
|---|---|
| Silent error rate | Silent errors ÷ tasks |
| Loud error rate | Loud errors ÷ tasks |
| **Escaped error rate** (headline) | Tasks where the harness **accepted** a wrong output ÷ tasks |
| Catch rate | Errors detected (disagreement raised) ÷ tasks where at least one programmer was wrong |
| Escalation rate | Escalations ÷ tasks. Also: share of escalations on tasks labeled ambiguous (should be high) |
| Adjudication accuracy | Correct verdicts ÷ adjudicated disagreements |
| Error correlation | P(B wrong ∣ A wrong); **same-wrong rate** = P(B's output identical to A's ∣ both wrong); Cohen's kappa on correctness |
| Cost per task | API-equivalent USD = tokens × list prices, counted for every call, including local ones (priced as if they were on an API, for comparison) |
| Ask rate (ambiguous tasks) | Escalated samples ÷ samples on ambiguous tasks. Baseline 0 of 75 (five models, harder round) |
| False-escalation rate | Escalated samples ÷ samples on clear tasks (baseline 0 of 90) |
| Unflagged-divergence rate | Samples on ambiguous tasks whose output differs from the oracle's reading and that did not escalate |
| Shared-choice rate | Of samples where two programmers both resolve an ambiguity silently, the share with identical outputs (same-family and cross-family) |
| Context tokens | Input tokens per task, a context-efficiency measure |
| Latency | Wall-clock time per task |

## Statistics

- Report n for everything. Use Wilson 95% confidence intervals for proportions.
- Compare configurations on the **same tasks** with a paired bootstrap over tasks (10,000 resamples) for differences in escaped error rate, and McNemar's test for paired correctness.
- With about 100 test tasks × 3 samples, report sample-level and task-level (majority or any-error) numbers, and say which is which.
- Never tune on `test` or `heldout`. If you do by accident, write it down in `09_DECISIONS.md` and in the write-up.

## Run protocol

1. Develop on `dev` with local models (free).
2. Freeze: tag `benchmark-v1.0` and the prompt templates.
3. Run every configuration on `test` and `heldout` **once**, with paid models through the Batch API where possible.
4. Rerun only for infrastructure failures, recorded in `STATUS.md`.

## Budget plan (paid runs only)

| Run | Estimate (VERIFY prices) |
|---|---|
| K2 (20 tasks, Sonnet plus Haiku) | about $1 |
| Dev iteration on Claude | Under $5. Develop mostly on local models |
| Final E0–E6 Claude configurations on test and heldout, batch plus caching | About $10–25 |
| **Total** | **Under $40**, the hard cap in `CLAUDE.md` |

Estimate the cost before every paid run (tokens per task × tasks × samples × price) and ask the project owner if it's over $2.

## Reporting

- **Main table:** configuration × {silent, loud, escaped, escalation, cost per task}, with confidence intervals.
- **Headline chart:** escaped error rate against cost per task, one point per configuration, showing the Pareto frontier.
- **Correlation heatmap:** same-wrong rate between every pair of models.
- **Error taxonomy:** a bar chart of error categories by model.
- **Standard versus controlled tasks** (memorization signal).
- **Three case studies:** a silent error, a caught error, and an error that escaped because both models were wrong the same way.
- Keep the actual numbers in `results/` and link them. The README shows only numbers that exist.
