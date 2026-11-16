# Tare: working notes for Claude Code

Tare is a research prototype by Tanish Rana. Engineering quality and honest results matter more than speed.

**One line:** independent AI double programming for clinical trial datasets, and a measurement of when it fails.

## What to read

| When | Read |
|---|---|
| First session ever | `docs/00_START_HERE.md`, then follow its reading order |
| Start of every session | `docs/STATUS.md` (where things stand) and this file |
| SDTM, ADaM, ADSL, baseline flags and other domain questions | `docs/02_DOMAIN_PRIMER.md` |
| Building the harness | `docs/03_ARCHITECTURE.md` |
| Building tasks, the oracle, scoring | `docs/04_BENCHMARK_SPEC.md` |
| Running experiments, metrics, statistics | `docs/05_EXPERIMENTS.md` |
| Training the small local model | `docs/06_TRAINING.md` |
| Installing and configuring the machine | `docs/07_SETUP.md` |
| Phases, kill tests, gates, risks | `docs/08_ROADMAP.md` |
| Why something was decided | `docs/09_DECISIONS.md` |
| Sources | `docs/10_REFERENCES.md` |

## Hard rules

1. **No invented numbers.** Every metric in the docs, README or posts must come from a logged run under `results/`. If something wasn't measured, say so.
2. **Money.** Use local models (Ollama) for development. Ask the project owner before any paid API run expected to cost more than $2. Log every paid run in the spend table in `docs/STATUS.md`. The total API budget is $40 unless the project owner raises it.
3. **Big downloads.** Ask before any download over 5 GB, such as models or Docker images.
4. **Sandbox.** Model-written code runs only inside the Docker sandbox: no network, inputs mounted read-only, CPU, memory and time limits. Never run model output directly on the host.
5. **Isolation.** A programmer's sandbox must never contain reference answers, oracle outputs, or the other programmer's code. This is a core claim of the project, so enforce it in code and cover it with tests.
6. **Credentials.** The harness calls models only through API keys (Anthropic, optionally OpenAI) or the local Ollama server. Never route harness traffic through Claude.ai or ChatGPT subscription logins, and never automate those websites. Keys live in `.env`, which is git-ignored.
7. **Licensing.** Don't use the `qs_metabolic` dataset from `pharmaversesdtm`. Write task specs in our own words, not copied from CDISC implementation guides. Never train models on Claude or GPT outputs.
8. **Claims.** This is a research prototype on public data. Never describe it as validated, GxP-compliant or ready for FDA submission.
9. **Verify flagged facts.** Anything marked `VERIFY` in the docs came from a secondary source or memory. Check it before relying on it, then update the doc with what you found.
10. **Ask, don't assume,** when a choice is costly or hard to undo: spending money, deleting data, changing the benchmark after it's frozen, or changing the project's scope.

## Working style

- Plan briefly, build the smallest useful step, test it, then record it.
- Prefer plain, explicit code. Python 3.12 with type hints, `ruff` and `pytest`. R scripts run through `Rscript`, with dependencies pinned by `renv`.
- Every run writes to its own directory under `results/`, along with a copy of its config, the git commit, package versions and every model call.
- Keep this file short and put detail in `docs/`. Research on coding agents found that long context files tend to hurt more than help.
- End every session by updating `docs/STATUS.md` (done, next, blockers, spend) and adding any decisions to `docs/09_DECISIONS.md`.
- Make small commits with descriptive messages. Never commit `data/`, `results/`, `.env` or model files.

## Machine

MacBook Pro, Apple M5, 32 GB unified memory, macOS. Plan on roughly 20–24 GB for a local model plus its context, so load one large model at a time. The Docker Desktop VM is capped at 4 GB. Model-written code runs in Docker. Ollama and MLX run natively, so they can use the GPU.

## Commands

- `make test` / `make lint`: unit tests and lint (no network, no API keys).
- `make setup-data`: export SDTM, build oracles (`Rscript r/oracle_build.R`), build task bundles and answer keys. `make references` checks every reference solution scores correct.
- `make sandbox-image` / `make sandbox-smoke`: build and check the Docker sandbox. `make ollama`: start the local model server (16k context).
- `.venv/bin/tare run --config configs/<name>.yaml`: one single-programmer experiment; writes `results/<timestamp>_<name>/`.
- `.venv/bin/python scripts/k3_correlation.py <run_dir> <run_dir>`: pairwise error correlation.
