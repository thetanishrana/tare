# Training the small local model (Phase 3, optional)

## Goal

Make a 1.7–4B local model a useful **independent programmer B**, for teams that can't send data off-site. Success means a measurable gain on held-out test tasks and a useful contribution as programmer B in the harness (E7 in `05_EXPERIMENTS.md`). A negative result, reported honestly, is still a result.

## Before starting (gate)

- K4 showed the base model gets **some** tasks right. Ideally 10–50% on dev-style tasks. At 0%, reinforcement learning has no signal; at nearly 100%, there's nothing to gain.
- Phases 1–2 are done and published. Training is an upgrade, not a dependency.

## Data rules

- **Never train on `test` or `heldout` tasks,** their oracle outputs, or close variants of them.
- **Never train on Claude or GPT outputs.** Provider terms may prohibit it, and it muddies the claim. Training targets come only from:
  1. the small model's **own** samples that passed the checker (rejection sampling, also called expert iteration), and
  2. optionally, human-written reference code adapted from the admiral templates. **VERIFY** admiral's license (believed Apache-2.0) and credit it.
- Generate training tasks the same way as benchmark tasks: new sponsor variants and perturbations on the **training** split of datasets and variables, each answered by the oracle. Keep a list of which variables and datasets are training-only.

## Stage A: supervised fine-tuning (SFT) by rejection sampling

1. For each training task, sample k = 8 solutions from the base model.
2. Run each in the sandbox and score it against the oracle.
3. Keep the correct solutions, at most 2 per task, deduplicated.
4. Fine-tune with LoRA on those (spec + data description → code).
5. Evaluate on dev, then on test once at the end.

## Stage B: GRPO with an execution-based reward

- **Reward** (computed outside the sandbox by comparing output with the oracle):
  - 1.0 if correct
  - partial credit: share of records correct, scaled to 0–0.5. Keep it below 1 so a mostly-right answer never beats a fully right one.
  - 0 for loud errors (no valid output)
  - a small penalty for exceeding the length limit or breaking the output format
- **Reward hacking to guard against:** outputs that copy inputs to match the expected shape, hard-coded values, reading files outside `inputs/` (impossible in the sandbox, so keep it that way), and printing instead of writing output. The contract checks plus the sandbox should block these. Inspect a sample of high-reward outputs by hand every few hundred steps.

## Tools

### On the Mac (preferred): `mlx-lm-lora`
- `pip install -U mlx-lm-lora`. Supports SFT, DPO, GRPO (and variants), LoRA, DoRA and QLoRA.
- **Custom rewards (VERIFY against the repo README):** write a Python file with a function decorated by `register_reward_function()`, pass it with `--reward-functions-file`, select it with `--reward-functions`. The function receives `prompts`, `completions`, `answer` and `types`, and must return one float per completion.
- Memory guidance from the repo: 1–3B models `--batch-size 4 --num-layers 16`; 7B `--batch-size 2 --num-layers 8 --load-in-8bits`; 13B and up `--batch-size 1 --num-layers 4 --load-in-4bits --grad-checkpoint`.
- The reward function has to run sandboxed code. Call the Tare sandbox and scorer from inside it, and cache results by code hash.
- **Measure throughput first:** time 10 GRPO steps. GRPO generates several completions per prompt every step, so real runs are probably overnight jobs. Keep the laptop plugged in.

### Fallback: Kaggle with Unsloth
- Kaggle gives about 30 free GPU hours a week (T4 or P100, 16 GB). Unsloth supports GRPO on small models with low memory.
- The reward needs code execution. On Kaggle, run R or Python in a subprocess with time and resource limits, since Docker isn't available there. Weaker isolation is acceptable for training only, because the training data is public. Never run test evaluation this way.

## Serving the trained model

- Fuse LoRA adapters into the base model with MLX, then serve with an MLX OpenAI-compatible server, or convert to GGUF and import into Ollama with a Modelfile. **VERIFY** the conversion path for the chosen model architecture.
- Register it in the model roster as `tare-small-<version>`.

## Evaluation

| Model | Dev | Test | Heldout | As programmer B (E7) |
|---|---|---|---|---|
| Base | | | | |
| SFT | | | | |
| SFT + GRPO | | | | |

Report confidence intervals, compute used (hours), and wall-clock time.

## Time budget

About 30–40 hours of work: data generation 8–10, SFT 6–8, GRPO 10–14, evaluation 4–6. Compute runs overnight.
